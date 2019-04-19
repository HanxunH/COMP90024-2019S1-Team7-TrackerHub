<template>
<div id="gmap" style="background-color:#bbb;">
    <div id="map_canvas" style="height: 100vh; width: 100%" ></div>
    <div id="chart" class="container-fluid w-100 d-inline-block" style="height: 100vh;z-index:0;background-color:#ccc;">
      <div class="row">
        <div class="col-lg-3"><Barchart/></div>
        <div class="col-lg-3"><Linechart/></div>
        <div class="col-lg-3"><Piechart/></div>
        <div class="col-lg-3"><Radarchart/></div>
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
      pieData: []
    }
  },

  mounted () {
     this.mapBuild()
  },

  created: function(){
  },

  methods: {
    mapBuild(){
      let self = this;
      let map = new google.maps.Map(document.getElementById('map_canvas'), {
        zoom: 13,
        center:  {lat: -37.8136, lng: 144.9631},
        disableDefaultUI: true,
        styles: mapStyle
      });
      
      map.data.loadGeoJson('https://api.myjson.com/bins/udv2g');
      map.data.setStyle(function(feature) {
        let cartodb_id = feature.getProperty('cartodb_id');
        let color = cartodb_id > 30 ? 'white' : 'gray';
        return {
          fillColor: color,
          strokeWeight: 1
        };
      });

      let infowindow = new google.maps.InfoWindow();

      // mouse click event: show grid info
      map.data.addListener('click', function(event) {
        // prepare data
        let name = event.feature.getProperty("name");
        let data1 = 1, data2 = 2, data3 = 3, data4 = 4;
        self.pieData = [data1, data2, data3, data4]
        // init infowindow with customized view
        let InfoWindow = Vue.extend(InfoWindowComponent);

        // send data to the view
        let instance = new InfoWindow({
          propsData: {
            name,
            pieData: self.pieData,
            data1,
            data2,
            data3,
            data4
          }
        });
        instance.$mount();

        infowindow.setContent(instance.$el);
        //infowindow.setPosition(event.feature.getGeometry().getAt(0).getAt(0).getAt(0));
        infowindow.setPosition(event.latLng)
        //infowindow.setOptions({pixelOffset: new google.maps.Size(0,0)});
        infowindow.open(map);
      });  
      
      // mouse over event: highlight color
      map.data.addListener('mouseover', function(event) {
        map.data.overrideStyle(event.feature, {fillColor: 'black'});
      });

      // mouse our event: reset color/info-window
      map.data.addListener('mouseout', function(event) {
        map.data.revertStyle();
        infowindow.close();
      });
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