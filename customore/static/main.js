// custom javascript
$(document).ready(() => {
  console.log('Sanity Check!');
});

$("#btnSubmit").click(function () {
  var key = $("#keyword").val();
  $.ajax({
    url: '/scrape/',
    data: { keyword: key },
    method: 'POST',
  })
    .done((res) => {
      getStatus(res.task_id);
    })
    .fail((err) => {
      console.log(err);
    });
});

function getStatus(taskID) {
  $.ajax({
    url: `/scrape/${taskID}/`,
    method: 'GET'
  })
    .done((res) => {
      const taskStatus = res.task_status;
      if (taskStatus === 'SUCCESS' || taskStatus === 'FAILURE') {
        if (taskStatus === 'SUCCESS') {
          brands = res.task_result['brands'];
          stats = res.task_result['stats'];
          orders = []
          for (var br in brands) {
            console.log(brands[br]);
            for (var n in stats) {
              if (brands[br] == stats[n]['brand']) {
                orders.push(stats[n]['share']);
              }
            }
          }
          var ctx = document.getElementById('myChart').getContext('2d');
          var chart = new Chart(ctx, {
            // The type of chart we want to create
            type: 'horizontalBar',
            // The data for our dataset
            data: {
              labels: brands,
              datasets: [{
                label: 'Share of Search in Lazada',
                backgroundColor: 'rgb(30,144,255)',
                borderColor: 'rgb(255, 99, 132)',
                data: orders
              }]
            },
            // Configuration options go here
            options: {}
          });
        }
        return false;
      }
      setTimeout(function () {
        console.log(getStatus(res.task_id));
      }, 1000);
    })
    .fail((err) => {
      console.log(err)
    });
}
