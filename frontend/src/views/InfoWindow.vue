<template>
  <div style="height:300px; weight:250px; min-width:250px; text-align:center;">
    <h4>{{name}}</h4>
    <Piechart
        :data="this.infoPieData"
    />
  </div>
</template>

<script>
import Piechart from './../components/Piechart'

export default {
    name: 'infowindow',
    props: [
        'name',
        'infoPieData',
    ],
    components: {
        Piechart
    }
}
</script>