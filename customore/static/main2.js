// custom javascript

$(document).ready(() => {
    console.log('Sanity Check!');
  });
  
  $('.button').on('click', function() {
    console.log('here')
    $.ajax({
      url: '/scrape/',
      data: { type: $(this).data('type') },
      method: 'POST',
    })
    .done((res) => {
      console.log('is done');
      console.log(res);
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
      const html = `
        <tr>
          <td>${res.task_id}</td>
          <td>${res.task_status}</td>
          <td>${res.task_result}</td>
        </tr>`
      $('#tasks').prepend(html);
  
      const taskStatus = res.task_status;
  
      if (taskStatus === 'SUCCESS' || taskStatus === 'FAILURE') return false;
      setTimeout(function() {
        getStatus(res.task_id);
      }, 1000);
    })
    .fail((err) => {
      console.log(err)
    });
  }
  