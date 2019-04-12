<template>
<div id='app' style="background-color:#bbb;">
  
    <div class="mw-100 h-10" >
      <div class="float-right">
        <b-button-group>
          <b-button>Button</b-button>
          <b-dropdown right text="Menu-1">
            <b-dropdown-item>Item 1</b-dropdown-item>
            <b-dropdown-item>Item 2</b-dropdown-item>
            <b-dropdown-divider></b-dropdown-divider>
            <b-dropdown-item>Item 3</b-dropdown-item>
          </b-dropdown>
          <b-dropdown right text="Menu-2">
            <b-dropdown-item>Item 1</b-dropdown-item>
            <b-dropdown-item>Item 2</b-dropdown-item>
            <b-dropdown-divider></b-dropdown-divider>
            <b-dropdown-item>Item 3</b-dropdown-item>
          </b-dropdown>
        </b-button-group>
      </div>
    </div>

    <div id="map_canvas" style="height: 500px; width: 100%"></div>

    <div class="container-fluid w-100 h-8 d-inline-block" style="z-index:0;background-color:#ccc;">
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
import Barchart from './components/Barchart.js'
import Linechart from './components/Linechart.js'
import Piechart from './components/Piechart.js'
import Radarchart from './components/Radarchart.js'
import {mapStyle} from './assets/js/map-style.js'

export default {
  name: 'app',
  components: {
    Radarchart,
    Piechart,
    Linechart,
    Barchart,
  },

  data() {
    return {
    }
  },

  mounted () {
     this.mapBuild()
  },

  created: function(){
  },

  methods: {
    mapBuild(){
      let map = new google.maps.Map(document.getElementById('map_canvas'), {
        zoom: 13,
        center:  {lat: -37.8136, lng: 144.9631},
        disableDefaultUI: true,
        styles: mapStyle
      });
      
      map.data.loadGeoJson('https://api.myjson.com/bins/udv2g');
      map.data.setStyle(function(feature) {
        var cartodb_id = feature.getProperty('cartodb_id');
        var color = cartodb_id > 30 ? 'white' : 'gray';
        return {
          fillColor: color,
          strokeWeight: 1
        };
      });

      let infowindow = new google.maps.InfoWindow();

      // mouse click event: show grid info
      map.data.addListener('click', function(event) {
        let myHTML = event.feature.getProperty("name");
        infowindow.setContent("<div style='width:150px; text-align: center;'>"+myHTML+"</div>");
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
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0px;
}
</style>