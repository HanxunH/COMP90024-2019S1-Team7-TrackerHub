import { Pie } from 'vue-chartjs'
 
export default {
  name:"Piechart",
  extends: Pie,
  mounted () {
    // Overwriting base render method with actual data.
    this.renderChart({
      labels: ['Teen','Big','Japanese','Nurse'],
      datasets: [
        {
          label: 'PornHub Commits',
          backgroundColor: ['#f8979', '#eee','#ddd','#888'],
          data: [40, 20, 30, 10]
        }
      ]
    })
  }
}


