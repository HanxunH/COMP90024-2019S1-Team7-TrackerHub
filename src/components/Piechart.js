import { Pie } from 'vue-chartjs'
 
export default {
  name:"Piechart",
  extends: Pie,
  mounted () {
    // Overwriting base render method with actual data.
    this.renderChart({
      labels: ['Teen','Big***','Japanese','Nurse'],
      datasets: [
        {
          label: 'PornHub Commits',
          backgroundColor: ['#f87979', '#ffff33','#ff9933','#66ffff'],
          data: [40, 20, 30, 10]
        }
      ]
    })
  }
}


