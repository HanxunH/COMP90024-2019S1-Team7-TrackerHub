<script>
import { Bar, mixins } from 'vue-chartjs'
const { reactiveProp } = mixins

export default {
  name:"Barchart",
  extends: Bar,
  mixins: [reactiveProp],
  props: [
    'height',
    'width',
    'chartData'
  ],
  mounted () {
    // Overwriting base render method with actual data.
    this.renderChart(this.chartData,{
      responsive: true, maintainAspectRatio: false 
    })
  }
}
</script>
