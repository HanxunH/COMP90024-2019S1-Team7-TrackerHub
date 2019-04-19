<template>
    <div style="height:300px; weight:250px; min-width:250px; text-align:center;">
        <h4>{{name}}</h4>
        <Piechart/>
    </div>
</template>

<script>
import Barchart from './../components/Barchart.js'
import Linechart from './../components/Linechart.js'
import Piechart from './../components/Piechart.js'
import Radarchart from './../components/Radarchart.js'

export default {
    name: 'infowindow',
    props: [ 
        'name',
        'data1',
        'data2',
        'data3',
        'data4'
    ],
    components: {
        Radarchart,
        Piechart,
        Linechart,
        Barchart,
    }
}
</script>