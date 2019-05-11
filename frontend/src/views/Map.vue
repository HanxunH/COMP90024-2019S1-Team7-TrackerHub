<template>
  <div id="gmap">
    <loading :active.sync="visible" :can-cancel="true"></loading>
    <!-- Map -->
    <div id="map_canvas" style="height: 100vh; width: 100%" ></div>
    <!-- Div on top of the map -->
    <div id="onmap">    
      <div class="container mt-3">
        <h2>User Track</h2>
        <p>Track user by user ID:</p>
        <input class="form-control" v-model="user_id" type="text" placeholder="Search..">
        <div id="myDIV" class="mt-3">
          <button class="btn btn-dark" :disabled="tags == null || tags == '' || user_id == ''" @click="mapBuildTrack()">Track</button>
        </div>
        <p></p>
      </div> 
        <div class="container mt-3">
        <p>Track random number of users:</p>
        <input class="form-control" v-model="number" type="number" placeholder="Search..">
        <br>
        <p>Skip:</p>
        <input class="form-control" v-model="skip" type="number" placeholder="Skip..">
        <div id="myDIV2" class="mt-3">
          <button class="btn btn-dark" :disabled="tags == null || tags == ''" @click="mapBuildTrackN()">Track</button>
        </div>
        <p></p>
        <div></div>
      </div>     
    </div>
    
    <!-- Charts -->
    <a class="anchor" id="anchor1"></a>
    <div id="chart" class="container-fluid w-100 d-inline-block" style="height: 100vh;z-index:0;">
      <div class="row">
        <div class="col-lg-12"><Barchart :chartData="this.barDatacollection" :height="700" :width="2000" /></div>
      </div>
      <div class="row">
        <div class="col-lg-12"><Barchart :chartData="this.barDatacollection" :height="700" :width="2000" /></div>
      </div>
      <div class="row">
        <div class="col-lg-3"><Linechart :data="this.lineData"/></div>
        <div class="col-lg-3"><Piechart :data="this.pieData"/></div>
        <div class="col-lg-3"><Linechart :data="this.lineData"/></div>
        <div class="col-lg-3"><Piechart :data="this.pieData"/></div>
      </div> 
    </div>  

    <!-- Tool Navbar -->
    <nav class="navbar fixed-bottom navbar-light">
      <div class="row" style="width: 100vw;">
        <div style="margin-left: 30px;">
          <span class="pull-left">
          <datetime v-model="start_time" :type="'date'" :title="'Select your start time'"></datetime>
          </span>
        </div>
        <div style="margin-left: 30px;">
          <a class="navbar-brand font-weight-bold text-white">To</a>
        </div>
        <div style="margin-left: 15px;">
          <datetime v-model="end_time" :type="'date'" :title="'Select your end time'"></datetime>
        </div>
        <div class="col-md-3">
          <sui-dropdown
            fluid
            multiple
            :options="selections"
            placeholder="Sins"
            selection
            v-model="tags"
          />
        </div>
        <div>
          <button class="btn btn-dark" 
            :disabled="tags == null || tags == '' ||
            start_time.includes('NaN') || start_time == '' ||
            end_time.includes('NaN') || end_time == ''" 
            @click="mapBuildTime()">Search
          </button>
        </div>
        <div class="col-md-4" style="height: 4vh; margin-bottom: 1vh;">
          <flash-message transitionIn="animated swing"></flash-message>
        </div>
      </div>
    </nav>

  </div>
</template>


<script>
import Barchart from './../components/Barchart'
import Linechart from './../components/Linechart'
import Piechart from './../components/Piechart'
import Radarchart from './../components/Radarchart'
import {mapStyle} from './../assets/js/map-style'
import {Const} from './../assets/js/const'
import InfoWindowComponent from './InfoWindow'
import Vue from 'vue'
import 'bootstrap/dist/css/bootstrap.css'
import {Datetime} from 'vue-datetime'
import 'vue-datetime/dist/vue-datetime.css'
import Loading from 'vue-loading-overlay'
import 'vue-loading-overlay/dist/vue-loading.css'

export default {
  name: 'gmap',
  components: {
    Radarchart,
    Piechart,
    Linechart,
    Barchart,
    datetime: Datetime,
    Loading
  },

  data() {
    return {
      visible: false,
      pieData: [4,5,6,7],
      barData: [],
      barDataLabel: [],
      radarData: [],
      lineData: [],
      barDatacollection: null,
      start_time: new Date().toString(),
      end_time: new Date().toString(),
      user_id: '',
      number: 1,
      skip: 0,
      melb_geo: 'https://data.gov.au/geoserver/vic-local-government-areas-psma-administrative-boundaries/wfs?request=GetFeature&typeName=ckan_bdf92691_c6fe_42b9_a0e2_a4cd716fa811&outputFormat=json',
      tags: null,
      selections: [
        { key: 'lust', text: 'Lust', value: 'lust' },
        { key: 'gluttony', text: 'Gluttony', value: 'gluttony' },
        { key: 'text', text: 'Text', value: 'text' },
        { key: 'sentiment', text: 'Sentiment', value: 'sentiment' }
      ],

    }
  },

  mounted () {
    this.mapInit()
    this.mapBuild()
  },
  
  methods: {
    // ========================== Init Map ===================================================
    mapInit(){
      let map = new google.maps.Map(document.getElementById('map_canvas'), {
        zoom: 13,
        center:  {lat: -37.7998, lng: 144.9460},
        disableDefaultUI: true,
        styles: mapStyle
      })  
    },
    // ========================== Build Map ==================================================
    mapBuild(){
      let map = new google.maps.Map(document.getElementById('map_canvas'), {
        zoom: 13,
        center:  {lat: -37.7998, lng: 144.9460},
        disableDefaultUI: true,
        styles: mapStyle
      })

      let infowindow = new google.maps.InfoWindow()
      let marker, i
      let markers = []
      let locations = []

      this.barDataLabel.length=0
      this.barData.length=0

      // ======================== Setup each region/ Collect bar data ==========================
      // set style for each region
      map.data.loadGeoJson(this.melb_geo)
      map.data.setStyle((feature) => {
        let total = feature.getProperty('cartodb_id')
        let name = feature.getProperty('vic_lga__3')
        //let tags = feature.getProperty('tags')
        if (!this.barDataLabel.includes(name)){
          this.barDataLabel.push(name)
          this.barData.push(total)
        }
       
        // let details = feature.getProperty('detail')
        // for (let detail in details) {
        //   locations.push([detail.tag,detail.coordinates[0],detail.coordinates[1]]) 
        // }
        let color = total > 30 ? 'white' : 'gray'
        return {
          fillColor: color,
          strokeWeight: 1
        }
      })

      // setup bar data
      this.barDatacollection = {
        labels: this.barDataLabel,
        datasets: [
          {
            label: 'Lust',
            backgroundColor: '#ff9900',
            data: this.barData
          }, {
            label: 'Gluttony',
            backgroundColor: '#DC143C',
            data: this.barData
          }
        ]
      }


      // ========================Icon examples=========================
      let icon = {
        path: Const.svg_lust,
        fillColor: '#ff9900',
        fillOpacity: 1,
        anchor: new google.maps.Point(250,250),
        strokeWeight: 0, 
        scale: .1
      }
            
      let icon2 = {
        path: Const.svg_gluttony,
        fillColor: '#ff9900',
        fillOpacity: 1,
        anchor: new google.maps.Point(250,250),
        strokeWeight: 0, 
        scale: .1
      }

      let icon3 = {
        path: Const.svg_neutral,
        fillColor: '#ff9900',
        fillOpacity: 1,
        anchor: new google.maps.Point(250,250),
        strokeWeight: 0, 
        scale: .1
      }
            
      let icon4 = {
        path: Const.svg_positive,
        fillColor: '#ff9900',
        fillOpacity: 1,
        anchor: new google.maps.Point(250,250),
        strokeWeight: 0, 
        scale: .1
      }

      let icon5 = {
        path: Const.svg_negative,
        fillColor: '#ff9900',
        fillOpacity: 1,
        anchor: new google.maps.Point(250,250),
        strokeWeight: 0, 
        scale: .1
      }

      let myFoodMark = {lat: -37.8036, lng: 144.9631}
      let myLustMark = {lat: -37.8136, lng: 144.9631}
      let myNormalMark = {lat: -37.8036, lng: 144.9531}
      let myPositiveMark = {lat: -37.8136, lng: 144.9731}
      let myNegativeMark = {lat: -37.8236, lng: 144.9631}

      let foodMark = new google.maps.Marker({
        position: myFoodMark,
        map: map,
        animation: google.maps.Animation.BOUNCE,
        title: 'Hello Food!',
        icon: icon2
      })

      let lustMark = new google.maps.Marker({
        position: myLustMark,
        map: map,
        animation: google.maps.Animation.BOUNCE,
        title: 'Hello Lust!',
        icon: icon
      })

      let warthMark = new google.maps.Marker({
        position: myNormalMark,
        map: map,
        animation: google.maps.Animation.BOUNCE,
        title: 'Hello Normal!',
        icon: icon3
      })

      let positiveMark = new google.maps.Marker({
        position: myPositiveMark,
        map: map,
        animation: google.maps.Animation.BOUNCE,
        title: 'Hello Positive!',
        icon: icon4
      })

      let negativeMark = new google.maps.Marker({
        position: myNegativeMark,
        map: map,
        animation: google.maps.Animation.BOUNCE,
        title: 'Hello Negative!',
        icon: icon5
      })

      positiveMark.addListener('click', function() {
        let content = '<div id="content" style="min-width:150px;">'+
                      '<p>Tags</p>'+
                      '<button class="btn btn-primary btn-dark">positive</button>'+
                      '<button class="btn btn-primary btn-warning">positive</button>'+
                      '<button class="btn btn-primary">positive</button>'+
                      '</div>';
        
        infowindow.setContent(content)
        infowindow.open(map, positiveMark)
      })

      //======================== Setup each mark ==========================
      /*
      // set marks on the map
      for (i = 0; i < locations.length; i++) {  
        marker = new google.maps.Marker({
          position: new google.maps.LatLng(locations[i][1], locations[i][2]), 
          map: map,
          visible: true, // or false. Whatever you need.
          icon: locations[i][3],
          zIndex: 10,
          visible: false
        });
        // Open marker on mouseover
        google.maps.event.addListener(marker, 'mouseover', (function(marker, i) {
          return function() {
            infowindow.setContent(locations[i][0])
            infowindow.open(map, marker)
          }
        })(marker, i))
        markers.push(marker) // save all markers
      }

      // Change markers on zoom
      google.maps.event.addListener(map, 'zoom_changed', function() {
          var zoom = map.getZoom();
          // iterate over markers and call setVisible
          for (i = 0; i < locations.length; i++) {
              markers[i].setVisible(zoom >= 15);
          }
      });
      */

      google.maps.event.addListener(map, 'zoom_changed', () => {
        let zoom = map.getZoom()
        // iterate over markers and call setVisible
        lustMark.setVisible(zoom >= 15)
      })

      // mouse click event: show grid info
      map.data.addListener('click', (event) => {
        // prepare data
        let name = event.feature.getProperty("vic_lga__3")
        // let infoPieData = [] 
        // let infoPieName = []
        // let total = event.feature.getProperty("total")
        // let tags = event.feature.getProperty("tag")
        // for (let tag in tags) {
        //    infoPieData.push(tag.count)
        //    infoPieData.push(tag.name)
        //}
        // set all chart data here
        let data1 = 1, data2 = 2, data3 = 3, data4 = 4
        let infoPieData = [data1, data2, data3, data4]
        // init infowindow with customized view
        let InfoWindow = Vue.extend(InfoWindowComponent)

        // send data to the view
        let instance = new InfoWindow({
          propsData: {
            name,
            infoPieData: infoPieData,
          }
        })
        instance.$mount()

        infowindow.setContent(instance.$el)
        //infowindow.setPosition(event.feature.getGeometry().getAt(0).getAt(0).getAt(0))
        infowindow.setPosition(event.latLng)
        //infowindow.setOptions({pixelOffset: new google.maps.Size(0,0)})
        infowindow.open(map)
      })
      
      // mouse over event: highlight color
      map.data.addListener('mouseover', (event) => {
        map.data.overrideStyle(event.feature, {fillColor: 'black'})
      })

      // mouse our event: reset color/info-window
      map.data.addListener('mouseout', (event) => {
        map.data.revertStyle()
        infowindow.close()
      })
    },

    // ====================== Get Map/Chart Data =============================================
    mapBuildTime() {
      this.visible = true
      let sDate = new Date(this.start_time)
      let eDate = new Date(this.end_time)
      
      let start_time = this.toISOLocal(sDate).replace(/T/g, " "),
          end_time = this.toISOLocal(eDate).replace(/T/g, " ")

      if (start_time.includes('NaN') || end_time.includes('NaN'))
        this.flash('Time must be selected', 'error')
      else {  
        let data = {
          start_time,
          end_time,
          tags: this.tags,
        }
      
        console.log(data)

        this.$ajax({
          url: `/api/statistics/time/`,
          method: 'POST',
          data: data
        }).then(res => {
            this.melb_geo = res.data.melb_geo,
            this.visible = false,
            console.log(this.melb_geo),
            // re-render the map here
            this.flash('success', 'success',{timeout: 3000}),
            this.mapBuild()
          })
          .catch(error => {
            this.visible = false,
            this.flash(`${error}`, 'error'),
            this.errored = true
        })   
      }  
    },

    // ====================== Track 1 User by ID =============================================
    mapBuildTrack(){
      this.visible = true
      let map = new google.maps.Map(document.getElementById('map_canvas'), {
        zoom: 13,
        center:  {lat: -37.7998, lng: 144.9460},
        disableDefaultUI: true,
        styles: mapStyle
      })

      let infowindow = new google.maps.InfoWindow()
      let path = []
      let sDate = new Date(this.start_time)
      let eDate = new Date(this.end_time)
      let start_time = this.toISOLocal(sDate).replace(/T/g, " "),
          end_time = this.toISOLocal(eDate).replace(/T/g, " ")
      let noData = false

      if (start_time.includes('NaN') || end_time.includes('NaN'))
        start_time = end_time = null
        
      let data = {
        start_time: '2016-01-09 10:00:00+1000',
        end_time: '2016-10-09 10:00:00+1000',
        tags: this.tags,
        skip: 0,
        threshold: 0.9,
        single: 20
      }
        
      console.log(data)

      this.$ajax({
        url: `/api/statistics/track/${this.user_id}/`,
        method: 'POST',
        data: data
      }).then(res => {

        console.log(res.data)
        
        if (Object.keys(res.data).length === 0)
          this.flash('no data match current query', 'error')
          noData = true

        for (const [key, value] of Object.entries(res.data)) {
          let point = {
            lat: value[0].geo[1], 
            lng: value[0].geo[0]
          }
          
          path.push(point)
          let svg_icon = Const.svg_neutral

          if (value[0].tags.sentiment){
            if (value[0].tags.sentiment[0] == 'positive'){
              svg_icon = Const.svg_positive
            }
            if (value[0].tags.sentiment[0] == 'negative'){
              svg_icon = Const.svg_negative
            }
          }

          let icon = {
            path: svg_icon,
            fillColor: '#ff9900',
            fillOpacity: 1,
            anchor: new google.maps.Point(250,250),
            strokeWeight: 0, 
            scale: .1
          }

          let marker = new google.maps.Marker({
            position: point,
            map: map,
            icon: icon,
            title: value[0].time
          })

          let tag_content = ''

          for (const [mainTag, subTags] of Object.entries(value[0].tags)){
            subTags.forEach(element => {
              tag_content = tag_content + `<button class="btn btn-primary btn-dark">${element}</button>`
            })
          }

          marker.addListener('click', () => {
            let content = '<div id="content" style="min-width:150px;">'+
                      '<h4 class="font-weight-bold">'+ key +'</h4>'+
                      tag_content+
                      '</div>'
            infowindow.setContent(content)
            infowindow.open(map, marker)
          })

          value.slice(1).forEach((track) => {
            svg_icon = Const.svg_neutral
            if (track.tags.sentiment){
              if (track.tags.sentiment[0] == 'positive'){
                svg_icon = Const.svg_positive
              }
              if (track.tags.sentiment[0] == 'negative'){
                svg_icon = Const.svg_negative
              }
            }

            let icon_sm= {
              path: svg_icon,
              fillColor: '#ff9900',
              fillOpacity: 1,
              anchor: new google.maps.Point(250,250),
              strokeWeight: 0, 
              scale: .05
            }

            point = {
              lat: track.geo[1], 
              lng: track.geo[0]
            }

            let marker = new google.maps.Marker({
              position: point,
              map: map,
              icon: icon_sm,
              title: track.time
            })

            tag_content = ''

            for (const [mainTag, subTags] of Object.entries(track.tags)){
              subTags.forEach(tag => {
                tag_content = tag_content + `<button class="btn btn-primary btn-dark">${tag}</button>`
              })
            }

            marker.addListener('click', () => {
              let content = '<div id="content" style="min-width:150px;">'+
                      '<p class="font-weight-bold">Tags</p>'+
                      tag_content+
                      '</div>'
              infowindow.setContent(content)
              infowindow.open(map, marker)
            })

            path.push(point)
          })
        }
      }).then(() => {
        let trackPath = new google.maps.Polyline({
          path: path,
          geodesic: true,
          strokeColor: '#ff9900',
          strokeOpacity: 1.0,
          strokeWeight: 2,
        })
        google.maps.event.addListener(trackPath, 'mouseover', () => {
          trackPath.setOptions({strokeWeight: 4})
        })
        google.maps.event.addListener(trackPath, 'mouseout', () => {
          trackPath.setOptions({strokeWeight: 2})
        })
        trackPath.setMap(map)
        if (noData == false)
          this.flash('tracking success', 'success',{timeout: 3000})
          this.flash('tracking success', 'success',{timeout: 3000})
        this.visible = false
      }).catch(error => {
        this.flash(`${error}`, 'error'),
        this.visible = false
        this.errored = true
      })
    },

    // ====================== Track random n users ===========================================
    mapBuildTrackN() {
      this.visible = true
      let map = new google.maps.Map(document.getElementById('map_canvas'), {
        zoom: 13,
        center:  {lat: -37.7998, lng: 144.9460},
        disableDefaultUI: true,
        styles: mapStyle
      })

      let infowindow = new google.maps.InfoWindow()
      let paths = []
      let colors = []
      let sDate = new Date(this.start_time)
      let eDate = new Date(this.end_time)
      let noData = false
      
      let start_time = this.toISOLocal(sDate).replace(/T/g, " "),
          end_time = this.toISOLocal(eDate).replace(/T/g, " ")

      if (start_time.includes('NaN') || end_time.includes('NaN'))
        start_time = end_time = null
        
      let data = {
        start_time: '2016-01-09 10:00:00+1000',
        end_time: '2016-10-09 10:00:00+1000',
        tags: this.tags,
        skip: parseInt(this.skip),
        threshold: 0.9,
        single: 20  
      }

      console.log(data)
      
      this.$ajax({
        url: `/api/statistics/track/random/${this.number}/`,
        method: 'POST',
        data: data
      }).then(res => {
        if (Object.keys(res.data).length === 0)
          this.flash('no data match current query', 'error')
          noData = true
        
        console.log(res.data)

        for (const [key, value] of Object.entries(res.data)) {
          let point = {
            lat: value[0].geo[1], 
            lng: value[0].geo[0]
          }
          let color = this.getRandomColor()
          let path = []
          path.push(point)
          colors.push(color)
          let svg_icon = Const.svg_neutral

          if (value[0].tags.sentiment){
            if (value[0].tags.sentiment[0] == 'positive'){
              svg_icon = Const.svg_positive
            }
            if (value[0].tags.sentiment[0] == 'negative'){
              svg_icon = Const.svg_negative
            }
          }
          
          let icon = {
            path: svg_icon,
            fillColor: color,
            fillOpacity: 1,
            anchor: new google.maps.Point(250,250),
            strokeWeight: 0, 
            scale: .1
          }

          let marker = new google.maps.Marker({
            position: point,
            map: map,
            icon: icon,
            title: value[0].time
          })

          let tag_content = ''

          for (const [mainTag, subTags] of Object.entries(value[0].tags)){
            subTags.forEach(tag => {
              tag_content = tag_content + `<button class="btn btn-primary btn-dark">${tag}</button>`
            })
          }

          marker.addListener('click', () => {
            let content = '<div id="content" style="min-width:150px;">'+
                      '<h4 class="font-weight-bold">'+ key +'</h4>'+
                      tag_content+
                      '</div>'
            infowindow.setContent(content)
            infowindow.open(map, marker)
          })

          value.slice(1).forEach((track) => {
            svg_icon = Const.svg_neutral
            if (track.tags.sentiment){
              if (track.tags.sentiment[0] == 'positive'){
                svg_icon = Const.svg_positive
              }
              if (track.tags.sentiment[0] == 'negative'){
                svg_icon = Const.svg_negative
              }
            }

            let icon_sm= {
              path: svg_icon,
              fillColor: color,
              fillOpacity: 1,
              anchor: new google.maps.Point(250,250),
              strokeWeight: 0, 
              scale: .05
            }

            point = {
              lat: track.geo[1], 
              lng: track.geo[0]
            }

            let marker = new google.maps.Marker({
              position: point,
              map: map,
              icon: icon_sm,
              title: track.time
            })

            let tag_content = ''

            for (const [mainTag, subTags] of Object.entries(track.tags)){
              subTags.forEach(tag => {
                tag_content = tag_content + `<button class="btn btn-primary btn-dark">${tag}</button>`
              })
            }

            marker.addListener('click', () => {
              let content = '<div id="content" style="min-width:150px;">'+
                        '<p class="font-weight-bold">Tags</p>'+
                        tag_content+
                        '</div>'
              infowindow.setContent(content)
              infowindow.open(map, marker)
            })

            path.push(point)
          })
          paths.push(path)
        }
      }).then(() => {
        paths.forEach((path,j) => {
          let trackPath = new google.maps.Polyline({
            path: path,
            geodesic: true,
            strokeColor: colors[j],
            strokeOpacity: 1.0,
            strokeWeight: 2,
          })
          google.maps.event.addListener(trackPath, 'mouseover', () => {
            trackPath.setOptions({strokeWeight: 4})
          })
          google.maps.event.addListener(trackPath, 'mouseout', () => {
            trackPath.setOptions({strokeWeight: 2})
          })
          trackPath.setMap(map)
        })
        if (noData == false)
          this.flash(`${paths.length} users found`, 'success',{timeout: 3000})
          this.flash(`${paths.length} users found`, 'success',{timeout: 3000})
        this.visible = false
      }).catch(error => {
        console.log(error)
        this.flash(`${error}`, 'error'),
        this.visible = false
        this.errored = true
      })
    },

    // ====================== Time formatter =================================================
    toISOLocal(d) {
      let z = n => (n<10? '0':'')+n;
      let off = d.getTimezoneOffset();
      let sign = off < 0? '+' : '-';
      off = Math.abs(off);

      return d.getFullYear() + '-' + z(d.getMonth()+1) + '-' +
            z(d.getDate()) + 'T' + z(d.getHours()) + ':'  + z(d.getMinutes()) + 
            ':' + z(d.getSeconds()) + sign + z(off/60|0) + z(off%60); 
    },

    // ====================== Color generator ================================================
    getRandomColor() {
      const letters = '0123456789ABCDEF';
      let color = '#';
      for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
      }
      return color;
    }
  }
}
</script>


<style>
@import '~bootstrap/dist/css/bootstrap.css';
@import '~bootstrap-vue/dist/bootstrap-vue.css';
#header #logo {
  background: url("../assets/images/logo_premium.png") center;
  background-size: contain;
  background-repeat: no-repeat;
  background-color: transparent;
  position: fixed;
  width: 12em;
  height: 6em;
  top: 0;
  left: 3em;
}
#gmap {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0px;
  background-color:#bbb;
  position: relative;
}
#onmap {
  background-color:#ff9900;
  position: absolute; 
  top: 100px; 
  right: 20px; 
  z-index: 9999; 
  border-radius: 25px;
}
a.anchor {
  display: block;
  position: relative;
  top: -6em;
  visibility: hidden;
}
</style>