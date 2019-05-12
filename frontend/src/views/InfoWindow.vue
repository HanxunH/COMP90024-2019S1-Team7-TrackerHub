<template>
  <div style="height:900px; weight:250px; min-width:250px; text-align:center;">
    <h4>{{name}}</h4>

    <h4></h4>
    <Piechart
      :pieData="this.pieDatacollection_sentiment"
    />

    <h4></h4>
    <Piechart
      :pieData="this.pieDatacollection"
    />
  </div>
</template>

<script>
import Piechart from './../components/Piechart'

export default {
    name: 'infowindow',
    props: [
        'name',
        'pieDatacollection',
        'pieDatacollection_sentiment'
    ],
    components: {
        Piechart
    }
}
</script>