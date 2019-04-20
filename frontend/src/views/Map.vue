<template>
<div id="gmap" style="background-color:#bbb;">
    <div id="map_canvas" style="height: 100vh; width: 100%" ></div>
    <div id="chart" class="container-fluid w-100 d-inline-block" style="height: 100vh;z-index:0;background-color:#ccc;">
      <div class="row">
        <div class="col-lg-3"><Barchart :data="this.barData"/></div>
        <div class="col-lg-3"><Linechart :data="this.lineData"/></div>
        <div class="col-lg-3"><Piechart :data="this.pieData"/></div>
        <div class="col-lg-3"><Radarchart :data="this.radarData"/></div>
      </div>    
    </div>  
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


export default {
  name: 'gmap',
  components: {
    Radarchart,
    Piechart,
    Linechart,
    Barchart,
  },

  data() {
    return {
      infoPieData: [],
      pieData: [],
      barData: [],
      radarData: [],
      lineData: []
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
      map.data.loadGeoJson('https://api.myjson.com/bins/udv2g')
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

    // ====================== Collect Data ======================
    /* ======= Get map data =======
    getMapData(){
    	axios
        .get('http://domain/api/map/mapData.json')
        .then(response => {
          return response.data
        })
        .catch(error => {
          console.log(error)
          this.errored = true
        })
    },
    */
    getBarData(){
      let self = this
    	axios
        .get('http://domain/api/bar/barData.json')
        .then(response => {
          self.barData = response.data
        })
        .catch(error => {
          console.log(error)
          this.errored = true
        })
    },
    getLineData(){
      let self = this
    	axios
        .get('http://domain/api/line/lineData.json')
        .then(response => {
          self.lineData = response.data
        })
        .catch(error => {
          console.log(error)
          this.errored = true
        })
    },
    getRadarchartData(){
      let self = this
    	axios
        .get('http://domain/api/radar/radarData.json')
        .then(response => {
          self.radarData = response.data
        })
        .catch(error => {
          console.log(error)
          this.errored = true
        })
    }  
  }
}
</script>


<style>
@import '~bootstrap/dist/css/bootstrap.css';
@import '~bootstrap-vue/dist/bootstrap-vue.css';
#map {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0px;
}
</style>