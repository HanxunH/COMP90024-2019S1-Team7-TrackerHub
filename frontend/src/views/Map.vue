<template>
  <div id="gmap">

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
            <b-dropdown-item href="#" @click="mapBuildTrack(['food'])">Food</b-dropdown-item>
            <b-dropdown-item href="#" @click="mapBuildTrack(['porn'])">Porn</b-dropdown-item>
            <b-dropdown-item href="#" @click="mapBuildTrack(['food','porn'])">Food and Porn</b-dropdown-item>
          </b-dropdown>
        </div>
        <p></p>
      </div>    
    </div>
    
    <!-- Charts -->
    <a class="anchor" id="anchor1"></a>
    <div id="chart" class="container-fluid w-100 d-inline-block" style="height: 100vh;z-index:0;background-color:#ccc;">
      <div class="row">
        <div class="col-lg-3"><Barchart :data="this.barData"/></div>
        <div class="col-lg-3"><Linechart :data="this.lineData"/></div>
        <div class="col-lg-3"><Piechart :data="this.pieData"/></div>
        <div class="col-lg-3"><Radarchart :data="this.radarData"/></div>
      </div>    
    </div>  

    <!-- Tool Navbar -->
    <nav class="navbar fixed-bottom navbar-light">
      <div class="row">
        <div class="col-md-3">
          <date-picker v-model="start_time" :config="options"></date-picker>
        </div>
        <div class="col-md-1">
          <a class="navbar-brand">To</a>
        </div>
        <div class="col-md-3">
          <date-picker v-model="end_time" :config="options"></date-picker>
        </div>
        <div class="col-md-2">
          <b-dropdown id="dropdown-dropup" split split-href="#foo/bar" dropup text="Sins" class="m-md">
            <b-dropdown-item href="#" @click="mapBuildTime(['food'])">Food</b-dropdown-item>
            <b-dropdown-item href="#" @click="mapBuildTime(['porn'])">Porn</b-dropdown-item>
            <b-dropdown-item href="#" @click="mapBuildTime(['food','porn'])">Food and Porn</b-dropdown-item>
          </b-dropdown>
        </div>
        <div class="col-md-2">
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
import 'bootstrap/dist/css/bootstrap.css';
import datePicker from 'vue-bootstrap-datetimepicker';
import 'pc-bootstrap4-datetimepicker/build/css/bootstrap-datetimepicker.css';

export default {
  name: 'gmap',
  components: {
    Radarchart,
    Piechart,
    Linechart,
    Barchart,
    datePicker
  },

  data() {
    return {
      infoPieData: [],
      pieData: [],
      barData: [],
      radarData: [],
      lineData: [],
      start_time: new Date(),
      end_time: new Date(),
      user_id: '',
      options: {
        format: 'DD/MM/YYYY',
        useCurrent: false,
      },
      melb_geo: 'https://api.myjson.com/bins/udv2g',
      API_KEY: '227415ba68c811e9b1a48c8590c7151e'
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
    // ====================== Build Map ======================
    mapBuild(){
      let self = this
      let map = new google.maps.Map(document.getElementById('map_canvas'), {
        zoom: 13,
        center:  {lat: -37.8136, lng: 144.9631},
        disableDefaultUI: true,
        styles: mapStyle
      })
      
      // let mapData = getBarData()
      map.data.loadGeoJson(this.melb_geo)
      map.data.setStyle((feature) => {
        let cartodb_id = feature.getProperty('cartodb_id')
        let color = cartodb_id > 30 ? 'white' : 'gray'
        return {
          fillColor: color,
          strokeWeight: 1
        }
      })

      let infowindow = new google.maps.InfoWindow()

      // mouse click event: show grid info
      map.data.addListener('click', (event) => {
        // prepare data
        let name = event.feature.getProperty("name")
        let data1 = 1, data2 = 2, data3 = 3, data4 = 4
        self.infoPieData = [data1, data2, data3, data4]
        // init infowindow with customized view
        let InfoWindow = Vue.extend(InfoWindowComponent)

        // send data to the view
        let instance = new InfoWindow({
          propsData: {
            name,
            infoPieData: self.infoPieData,
            data1,
            data2,
            data3,
            data4
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
      console.log(self.start_time)
      console.log(self.end_time)
      console.log(tag)

      /* get data from server
      axios
        .get(`http://172.0.0.1:8080/api/statistics/time/`,{
          params:{
            start_time: self.start_time,
            end_time: self.end_time,
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
          self.melb_geo = response.data.melb_geo
          self.barData = response.data.barData
          self.lineData = response.data.lineData
          self.radarData = response.data.radarData
        })
        .catch(error => {
          console.log(error)
          this.errored = true
      })
      */

      // re-render the map here
      // this.mapBuild()
    },

    mapBuildTrack(tag){
      let self = this
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
      let time = new Date()
      let img = ''
      let tags = []
      /* get data from server
      axios
        .get(`http://172.0.0.1:8080/api/statistics/track/:user_id/`,{
          params:{
            user_id: self.user_id
          }
        },
        {
          headers: {
            'Content-Type': 'application/json',
            'X-API-KEY': self.API_KEY
          }
        })
        .then(response => {
          path = response.data.geo
          time = response.data.time
          img = response.data.img
          tags = response.data.tags
        })
        .catch(error => {
          console.log(error)
          this.errored = true
      })
      */

      let trackPath = new google.maps.Polyline({
        path: path,
        geodesic: true,
        strokeColor: '#FF0000',
        strokeOpacity: 1.0,
        strokeWeight: 2
      });

      trackPath.setMap(map);
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
  background-color:rgb(255, 153, 0);
  position: absolute; 
  top: 100px; 
  right: 20px; 
  z-index: 20099; 
  border-radius: 25px;
}
a.anchor {
  display: block;
  position: relative;
  top: -6em;
  visibility: hidden;
}
</style>