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
            <b-dropdown-item href="#" @click="mapBuildTrack(['food'])">Gluttony</b-dropdown-item>
            <b-dropdown-item href="#" @click="mapBuildTrack(['lust'])">Lust</b-dropdown-item>
            <b-dropdown-item href="#" @click="mapBuildTrack(['food','porn'])">Gluttony and Lust</b-dropdown-item>
          </b-dropdown>
        </div>
        <p></p>
      </div> 
        <div class="container mt-3">
        <p>Track random number of users:</p>
        <input class="form-control" v-model="number" type="number" placeholder="Search..">
        <div id="myDIV2" class="mt-3">
          <b-dropdown id="dropdown-1" split split-href="#foo/bar" text="Track" class="m-md">
            <b-dropdown-item href="#" @click="mapBuildTrackN(['lust'])">Gluttony</b-dropdown-item>
            <b-dropdown-item href="#" @click="mapBuildTrackN(['gluttony'])">Lust</b-dropdown-item>
            <b-dropdown-item href="#" @click="mapBuildTrackN(['warth'])">Warth</b-dropdown-item>
            <b-dropdown-item href="#" @click="mapBuildTrackN(['lust','gluttony','warth'])">All</b-dropdown-item>
          </b-dropdown>
        </div>
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
          <datetime v-model="start_time" :type="'datetime'" :title="'Select your start time'"></datetime>
        </div>
        <div class="col-md-1">
          <a class="navbar-brand font-weight-bold text-white">To</a>
        </div>
        <div class="col-md-4">
          <datetime v-model="end_time" :type="'datetime'" :title="'Select your end time'"></datetime>
        </div>
        <div class="col-md-2">
          <b-dropdown id="dropdown-dropup" size="sm" split split-href="#foo/bar" dropup text="Sins" class="m-md">
            <b-dropdown-item href="#" @click="mapBuildTime(['food'])">Gluttony</b-dropdown-item>
            <b-dropdown-item href="#" @click="mapBuildTime(['porn'])">Lust</b-dropdown-item>
            <b-dropdown-item href="#" @click="mapBuildTime(['food','porn'])">Gluttony and Lust</b-dropdown-item>
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
// Import component
import Loading from 'vue-loading-overlay';
// Import stylesheet
import 'vue-loading-overlay/dist/vue-loading.css';
import http from '../utils/http'
import api from '../utils/api'

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
      options: {
        format: 'DD/MM/YYYY',
        useCurrent: false,
      },
      melb_geo: 'https://api.myjson.com/bins/udv2g',
      API_KEY: '227415ba68c811e9b1a48c8590c7151e',
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
      let self = this
      let map = new google.maps.Map(document.getElementById('map_canvas'), {
        zoom: 13,
        center:  {lat: -37.8136, lng: 144.9631},
        disableDefaultUI: true,
        styles: mapStyle
      })
      let infowindow = new google.maps.InfoWindow()
      let marker, i
      let markers = []
      let locations = []
      console.log(self.barData)
      self.barDataLabel.length=0
      self.barData.length=0

      // ======================== Setup each region/ Collect bar data ==========================
      // set style for each region
      map.data.loadGeoJson(this.melb_geo)
      map.data.setStyle((feature) => {
        let cartodb_id = feature.getProperty('cartodb_id')
        let name = feature.getProperty('name')
        if (!self.barDataLabel.includes(name)){
          self.barDataLabel.push(name)
          self.barData.push(cartodb_id)
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
      self.barDatacollection = {
          labels: self.barDataLabel,
          datasets: [
            {
              label: 'Lust',
              backgroundColor: '#ff9900',
              data: self.barData
            }, {
              label: 'Gluttony',
              backgroundColor: '#DC143C',
              data: self.barData
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
      let self = this
      self.visible = true
      let sDate = new Date(self.start_time)
      let eDate = new Date(self.end_time)
      console.log(self.toISOLocal(sDate).replace(/T/g, " "))
      console.log(self.toISOLocal(eDate).replace(/T/g, " "))
      console.log(tag)
      
      this.$axios
        .get(`/api/statistics/time/`,{
            'start_time': self.toISOLocal(sDate).replace(/T/g, " "),
            'end_time': self.toISOLocal(eDate).replace(/T/g, " "),
            'tags': tag
        },
        
        )
        .then(response => (
          self.melb_geo = response.data.melb_geo,
          self.visible = false,
          console.log(self.melb_geo),
          // re-render the map here
          self.mapBuild()
        ))
        .catch(error => {
          self.visible = false,
          console.log(error),
          alert(error),
          this.errored = true
      })     
    },

    mapBuildTrack(tag){
      let self = this
      self.visible = true
      let map = new google.maps.Map(document.getElementById('map_canvas'), {
        zoom: 13,
        center:  {lat: -37.8136, lng: 144.9631},
        disableDefaultUI: true,
        styles: mapStyle
      })
      let infowindow = new google.maps.InfoWindow()
      let marker

      let path = [{lat: -37.8136, lng: 144.9631},
          {lat: 21.291, lng: -157.821},
          {lat: -18.142, lng: 178.431},
          {lat: -27.467, lng: 153.027}]
      let time = new Date()
      let img = ''
      let tags = []
      let sDate = new Date(self.start_time)
      let eDate = new Date(self.end_time)

      this.$axios
        .get(`http://172.26.38.1:8080/api/statistics/track/${self.user_id}/`,{
          data:{
            start_time: self.toISOLocal(sDate).replace(/T/g, " "),
            end_time: self.toISOLocal(eDate).replace(/T/g, " "),
            tags: tag
          }
        },
        {
          headers: {
            'Content-Type': 'application/json',
            'X-API-KEY': self.API_KEY
          }
        })
        .then(response => {
          // for (let point in response.data.(self.user_id)) {
          //   path.push({lat:point.geo[0], lng:point.geo[1]})
          //   marker = new google.maps.Marker({
          //     position: {lat:point.geo[0], lng:point.geo[1]},
          //     map: map,
          //     icon: point.img
          //     title: point.time+" "+point.tags
          //   })
          // }
          self.visible = false
          let trackPath = new google.maps.Polyline({
            path: path,
            geodesic: true,
            strokeColor: '#FF0000',
            strokeOpacity: 1.0,
            strokeWeight: 2
          })
          trackPath.setMap(map)
        })
        .catch(error => {
          self.visible = false
          alert(error)
          console.log(error)
          this.errored = true
      })
    },

    mapBuildTrackN(tag) {
      this.visible = true
      let map = new google.maps.Map(document.getElementById('map_canvas'), {
        zoom: 13,
        center:  {lat: -37.8136, lng: 144.9631},
        disableDefaultUI: true,
        styles: mapStyle
      })

      let path = [{lat: -37.8136, lng: 144.9631},
          {lat: 21.291, lng: -157.821},
          {lat: -18.142, lng: 178.431},
          {lat: -27.467, lng: 153.027}]

      let sDate = new Date(this.start_time)
      let eDate = new Date(this.end_time)
      console.log(tag)
      console.log(this.toISOLocal(sDate).replace(/T/g, " "))
      console.log(this.toISOLocal(eDate).replace(/T/g, " "))
      
      let data = {
        start_time: this.toISOLocal(sDate).replace(/T/g, " "),
        end_time: this.toISOLocal(eDate).replace(/T/g, " "),
        tags: tag,
        skip: 0,
        threshold: 0.9  
      }
      
      // 方法1 (错了，用方法2吧。。。)
    //  this.$ajax({
		// 		method: 'GET', 
		// 		url: `/api/statistics/track/random/${this.number}/`, 
		// 		data: data,
		// 	}).then(res => {
    //     console.log(res)
		// 	}, error => {
    //     console.log('error')
    //   })


      // 方法2 （返回500）
      this.$axios
        .get(`/api/statistics/track/random/${this.number}/`,{
          data: data,
        }).then(res => {
          console.log(res)
        }, error => {
          console.log('error')
        })




      // this.$axios
      //   .get(`http://172.26.38.1:8080/api/statistics/track/random/${self.number}/`,{
      //     data:{
      //       start_time: self.toISOLocal(sDate).replace(/T/g, " "),
      //       end_time: self.toISOLocal(eDate).replace(/T/g, " "),
      //       tags: tag
      //     }
      //   })
      //   .then(response => {
      //     for (let user in response.data) {
      //       for (let point in user){
      //         path.push({lat:point.geo[0], lng:point.geo[1]})
      //         marker = new google.maps.Marker({
      //           position: {lat:point.geo[0], lng:point.geo[1]},
      //           map: map,
      //           //icon: point.img,
      //           title: point.time+" "+point.tags
      //         })
      //       }
      //     }
      //     let trackPath = new google.maps.Polyline({
      //       path: path,
      //       geodesic: true,
      //       strokeColor: '#FF0000',
      //       strokeOpacity: 1.0,
      //       strokeWeight: 2
      //     })

      //     trackPath.setMap(map)
      //     self.visible = false
      //   })
      //   .catch(error => {
      //     self.visible = false
      //     alert(error)
      //     console.log(error)
      //     this.errored = true
      // })


    },

    toISOLocal(d) {
      let z = n => (n<10? '0':'')+n;
      let off = d.getTimezoneOffset();
      let sign = off < 0? '+' : '-';
      off = Math.abs(off);

      return d.getFullYear() + '-' + z(d.getMonth()+1) + '-' +
            z(d.getDate()) + 'T' + z(d.getHours()) + ':'  + z(d.getMinutes()) + 
            ':' + z(d.getSeconds()) + sign + z(off/60|0) + z(off%60); 
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