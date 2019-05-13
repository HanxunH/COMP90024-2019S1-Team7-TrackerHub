<script>
import { Pie, mixins } from 'vue-chartjs'
const { reactiveProp } = mixins

export default {
  name:"Piechart",
  extends: Pie,
  props: [
    'name',
    'pieData'
  ],
  mounted () {
    this.$nextTick(() => {
      // Overwriting base render method with actual data.
      this.renderChart(this.pieData,{
        responsive: true, maintainAspectRatio: false 
      })
    })
  },
  watch: {
    pieData: function(New,Old){
      this.renderChart(New,{
        responsive: true, maintainAspectRatio: false 
      })
    }
  }
}
</script>
