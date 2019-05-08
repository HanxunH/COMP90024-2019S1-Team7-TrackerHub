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
          <b-dropdown id="dropdown-1" split split-href="#foo/bar" text="Track" class="m-md">
            <b-dropdown-item href="#" @click="mapBuildTrack(['gluttony'])">Gluttony</b-dropdown-item>
            <b-dropdown-item href="#" @click="mapBuildTrack(['lust'])">Lust</b-dropdown-item>
            <b-dropdown-item href="#" @click="mapBuildTrack(['gluttony','porn'])">Gluttony and Lust</b-dropdown-item>
          </b-dropdown>
        </div>
        <p></p>
      </div> 
        <div class="container mt-3">
        <p>Track random number of users:</p>
        <input class="form-control" v-model="number" type="number" placeholder="Search..">
        <div id="myDIV2" class="mt-3">
          <b-dropdown id="dropdown-1" split split-href="#foo/bar" text="Track" class="m-md">
            <b-dropdown-item href="#" @click="mapBuildTrackN(['gluttony'])">Gluttony</b-dropdown-item>
            <b-dropdown-item href="#" @click="mapBuildTrackN(['lust'])">Lust</b-dropdown-item>
            <b-dropdown-item href="#" @click="mapBuildTrackN(['warth'])">Warth</b-dropdown-item>
            <b-dropdown-item href="#" @click="mapBuildTrackN(['lust','gluttony','warth'])">All</b-dropdown-item>
          </b-dropdown>
        </div>
        <Dropdown addClass="selection" name="selection" defaultText="请选择"
          v-model="selectedValue" :options="select_options"
          textFiled="value" valueFiled="id"
          @dropdown-selected="(text) => { selectedText = text}"
        ></Dropdown>
        <p></p>
      </div>     
    </div>
    
    <!-- Charts -->
    <a class="anchor" id="anchor1"></a>
    <div id="chart" class="container-fluid w-100 d-inline-block" style="height: 100vh;z-index:0;">
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
      <div class="row">
        <div class="col-md-4">
          <datetime v-model="start_time" :type="'date'" :title="'Select your start time'"></datetime>
        </div>
        <div class="col-md-1">
          <a class="navbar-brand font-weight-bold text-white">To</a>
        </div>
        <div class="col-md-4">
          <datetime v-model="end_time" :type="'date'" :title="'Select your end time'"></datetime>
        </div>
        <div class="col-md-2">
          <b-dropdown id="dropdown-dropup" size="sm" split split-href="#foo/bar" dropup text="Sins" class="m-md">
            <b-dropdown-item href="#" @click="mapBuildTime(['gluttony'])">Gluttony</b-dropdown-item>
            <b-dropdown-item href="#" @click="mapBuildTime(['lust'])">Lust</b-dropdown-item>
            <b-dropdown-item href="#" @click="mapBuildTime(['gluttony','lust'])">Gluttony and Lust</b-dropdown-item>
          </b-dropdown>
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
import InfoWindowComponent from './InfoWindow'
import Vue from 'vue'
import 'bootstrap/dist/css/bootstrap.css'
import {Datetime} from 'vue-datetime'
import 'vue-datetime/dist/vue-datetime.css'
import Loading from 'vue-loading-overlay'
import 'vue-loading-overlay/dist/vue-loading.css'
import Dropdown from 'vue-semantic-dropdown'

export default {
  name: 'gmap',
  components: {
    Radarchart,
    Piechart,
    Linechart,
    Barchart,
    datetime: Datetime,
    Loading,
    Dropdown
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
      options: {
        format: 'DD/MM/YYYY',
        useCurrent: false,
      },
      melb_geo: 'https://api.myjson.com/bins/udv2g',
      API_KEY: '227415ba68c811e9b1a48c8590c7151e',
      select_options: [
            {
                id: 'litteRed',
                value: '小红'
            },
            {
                id: 'litteBlue',
                value: '小蓝'
            }
        ],
      selectedValue: null,
      selectedText: null
    }
  },

  mounted () {
    this.mapBuild()
    
    /* Get chart data through API cals
    this.getBarData(),
    this.getLineData(),
    this.getRadarchartData()
    */
  },

  created: function(){

  },

  methods: {
    // ========================== Build Map ====================================================
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
      console.log(this.barData)
      this.barDataLabel.length=0
      this.barData.length=0

      // ======================== Setup each region/ Collect bar data ==========================
      // set style for each region
      map.data.loadGeoJson(this.melb_geo)
      map.data.setStyle((feature) => {
        let cartodb_id = feature.getProperty('cartodb_id')
        let name = feature.getProperty('name')
        if (!this.barDataLabel.includes(name)){
          this.barDataLabel.push(name)
          this.barData.push(cartodb_id)
        }
       
        // let total = feature.getProperty("total")
        // let details = feature.getProperty('detail')
        // for (let detail in details) {
        //   locations.push([detail.tag,detail.coordinates[0],detail.coordinates[1]]) 
        // }
        let color = cartodb_id > 30 ? 'white' : 'gray'
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

      let myFoodMark = {lat: -37.8036, lng: 144.9631}
      let foodMark = new google.maps.Marker({
        position: myFoodMark,
        map: map,
        animation: google.maps.Animation.BOUNCE,
        title: 'Hello Food!',
        icon: 'http://i64.tinypic.com/egzm07.png'
      })

      let myLustMark = {lat: -37.8136, lng: 144.9631}
      let lustMark = new google.maps.Marker({
        position: myLustMark,
        map: map,
        animation: google.maps.Animation.BOUNCE,
        title: 'Hello Lust!',
        icon: 'http://i68.tinypic.com/2rdfbsx.png',
        visible: false
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
        let name = event.feature.getProperty("name")
        // let total = event.feature.getProperty("total")
        // let tag = event.feature.getProperty("tag")
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

    // ====================== Get Map/Chart Data =====================
    mapBuildTime(tag) {
      this.visible = true
      let sDate = new Date(this.start_time)
      let eDate = new Date(this.end_time)
      console.log(this.toISOLocal(sDate).replace(/T/g, " "))
      console.log(this.toISOLocal(eDate).replace(/T/g, " "))
      console.log(tag)

      let data = {
        start_time: '2015-05-08 13:38:00+1000',
        end_time: '2016-05-08 13:39:00+1000',
        tags: tag,
        skip: 0,
        threshold: 0.9  
      }
      
      this.$ajax({
        url: `/api/statistics/track/${this.user_id}/`,
        method: 'GET',
        data: data
      }).then(res => {
          this.melb_geo = response.data.melb_geo,
          this.visible = false,
          console.log(this.melb_geo),
          // re-render the map here
          this.mapBuild()
        })
        .catch(error => {
          this.visible = false,
          console.log(error),
          alert(error),
          this.errored = true
      })     
    },

    mapBuildTrack(tag){
      this.visible = true
      let map = new google.maps.Map(document.getElementById('map_canvas'), {
        zoom: 13,
        center:  {lat: -37.7998, lng: 144.9460},
        disableDefaultUI: true,
        styles: mapStyle
      })

      let infowindow = new google.maps.InfoWindow()
      let path = []
      let marker
      let img = ''
      let tags = []
      let time = new Date()
      let sDate = new Date(this.start_time)
      let eDate = new Date(this.end_time)

      console.log(tag)
      console.log(this.toISOLocal(sDate).replace(/T/g, " "))
      console.log(this.toISOLocal(eDate).replace(/T/g, " "))
      
      let data = {
        start_time: '2015-05-08 13:38:00+1000',
        end_time: '2016-05-08 13:39:00+1000',
        tags: tag,
        skip: 0,
        threshold: 0.9  
      }

      this.$ajax({
        url: `/api/statistics/track/${this.user_id}/`,
        method: 'GET',
        data: data
      }).then(res => {
        for (const [key, value] of Object.entries(res.data)) {
          for (var i = 0; i < value.length; i++) {
            let point = {
              lat: value[i].geo[1], 
              lng: value[i].geo[0]
            }

            path.push(point)
            marker = new google.maps.Marker({
              position: point,
              map: map,
              animation: google.maps.Animation.BOUNCE,
              icon: 'http://i68.tinypic.com/2rdfbsx.png',
              title: value[i].time+" "+value[i].tags
            })
          }
        }
      }).then(() => {
        console.log(path);
        let trackPath = new google.maps.Polyline({
          path: path,
          geodesic: true,
          strokeColor: '#FF0000',
          strokeOpacity: 1.0,
          strokeWeight: 2,
        })
        trackPath.setMap(map)
        this.visible = false
      }).catch(error => {
        console.log(error)
        alert(error)
        this.visible = false
        this.errored = true
      })
    },

    mapBuildTrackN(tag) {
      this.visible = true
      let map = new google.maps.Map(document.getElementById('map_canvas'), {
        zoom: 13,
        center:  {lat: -37.7998, lng: 144.9460},
        disableDefaultUI: true,
        styles: mapStyle
      })

      let paths = []
      let colors = []
      let marker
      let sDate = new Date(this.start_time)
      let eDate = new Date(this.end_time)

      console.log(tag)
      
      let start_time = this.toISOLocal(sDate).replace(/T/g, " "),
          end_time = this.toISOLocal(eDate).replace(/T/g, " ")

      if (start_time.includes('NaN') || end_time.includes('NaN'))
        start_time = end_time = null
        
      let data = {
        start_time,
        end_time,
        tags: ['emotion','lust','gluttony'],
        skip: 0,
        threshold: 0.95,
        single: 20  
      }

      console.log(data)
      
      this.$ajax({
        url: `/api/statistics/track/random/${this.number}/`,
        method: 'POST',
        data: data
      }).then(res => {
        for (const [key, value] of Object.entries(res.data)) {
          let point = {
            lat: value[0].geo[1], 
            lng: value[0].geo[0]
          }
          let color = this.getRandomColor()
          let path = []
          colors.push(color)

          let icon = {
            path: 'M353.6 304.6c-25.9 8.3-64.4 13.1-105.6 13.1s-79.6-4.8-105.6-13.1c-9.8-3.1-19.4 5.3-17.7 15.3 7.9 47.2 71.3 80 123.3 80s115.3-32.9 123.3-80c1.6-9.8-7.7-18.4-17.7-15.3zm-152.8-48.9c4.5 1.2 9.2-1.5 10.5-6l19.4-69.9c5.6-20.3-7.4-41.1-28.8-44.5-18.6-3-36.4 9.8-41.5 27.9l-2 7.1-7.1-1.9c-18.2-4.7-38.2 4.3-44.9 22-7.7 20.2 3.8 41.9 24.2 47.2l70.2 18.1zm188.8-65.3c-6.7-17.6-26.7-26.7-44.9-22l-7.1 1.9-2-7.1c-5-18.1-22.8-30.9-41.5-27.9-21.4 3.4-34.4 24.2-28.8 44.5l19.4 69.9c1.2 4.5 5.9 7.2 10.5 6l70.2-18.2c20.4-5.3 31.9-26.9 24.2-47.1zM248 8C111 8 0 119 0 256s111 248 248 248 248-111 248-248S385 8 248 8zm0 448c-110.3 0-200-89.7-200-200S137.7 56 248 56s200 89.7 200 200-89.7 200-200 200z',
            fillColor: color,
            fillOpacity: 1,
            anchor: new google.maps.Point(250,250),
            strokeWeight: 0, 
            scale: .1
          }

          marker = new google.maps.Marker({
            position: point,
            map: map,
            icon: icon,
            title: value[0].time+" "+value[0].tags
          })

          for (let i = 0; i < value.length; i++) {
            let icon_sm= {
              path: 'M353.6 304.6c-25.9 8.3-64.4 13.1-105.6 13.1s-79.6-4.8-105.6-13.1c-9.8-3.1-19.4 5.3-17.7 15.3 7.9 47.2 71.3 80 123.3 80s115.3-32.9 123.3-80c1.6-9.8-7.7-18.4-17.7-15.3zm-152.8-48.9c4.5 1.2 9.2-1.5 10.5-6l19.4-69.9c5.6-20.3-7.4-41.1-28.8-44.5-18.6-3-36.4 9.8-41.5 27.9l-2 7.1-7.1-1.9c-18.2-4.7-38.2 4.3-44.9 22-7.7 20.2 3.8 41.9 24.2 47.2l70.2 18.1zm188.8-65.3c-6.7-17.6-26.7-26.7-44.9-22l-7.1 1.9-2-7.1c-5-18.1-22.8-30.9-41.5-27.9-21.4 3.4-34.4 24.2-28.8 44.5l19.4 69.9c1.2 4.5 5.9 7.2 10.5 6l70.2-18.2c20.4-5.3 31.9-26.9 24.2-47.1zM248 8C111 8 0 119 0 256s111 248 248 248 248-111 248-248S385 8 248 8zm0 448c-110.3 0-200-89.7-200-200S137.7 56 248 56s200 89.7 200 200-89.7 200-200 200z',
              fillColor: color,
              fillOpacity: 1,
              anchor: new google.maps.Point(250,250),
              strokeWeight: 0, 
              scale: .03
            }

            if (i != 0) {
              marker = new google.maps.Marker({
                position: point,
                map: map,
                icon: icon_sm,
                title: value[i].time+" "+value[i].tags
              })
            }
            
            point = {
              lat: value[i].geo[1], 
              lng: value[i].geo[0]
            }
            path.push(point)
          }
          paths.push(path)
        }
      }).then((res) => {
        for (let j = 0; j < paths.length; j++) {
          let trackPath = new google.maps.Polyline({
            path: paths[j],
            geodesic: true,
            strokeColor: colors[j],
            strokeOpacity: 1.0,
            strokeWeight: 2,
          })
          trackPath.setMap(map)
        }
        this.visible = false
      }).catch(error => {
        console.log(error)
        alert(error)
        this.visible = false
        this.errored = true
      })
    },

    toISOLocal(d) {
      let z = n => (n<10? '0':'')+n;
      let off = d.getTimezoneOffset();
      let sign = off < 0? '+' : '-';
      off = Math.abs(off);

      return d.getFullYear() + '-' + z(d.getMonth()+1) + '-' +
            z(d.getDate()) + 'T' + z(d.getHours()) + ':'  + z(d.getMinutes()) + 
            ':' + z(d.getSeconds()) + sign + z(off/60|0) + z(off%60); 
    },

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