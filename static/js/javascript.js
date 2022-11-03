$(document).ready(function () {
      $('#table1').DataTable({
        buttons: [
          { extend: 'excel', text: 'Download Excel' }
        ],
        "scrollY": '100%',
        "autoWidth": true,
        "autoHeight": true,
        sDom: "lBfrtip",
        "scrollY": '350px',

      });

      $(".detail").click(function () {

        var modalDiv = $("#model-div");
        var id = $(this).data(id);
        var csrftoken = '{{ csrf_token }}';
        $.ajax({
          type: "POST",
          url: "{% url 'detail' %}",
          headers: { 'X-CSRFToken': csrftoken },
          data: id,
          success: function (data) {
            debugger;
            console.log(data);
            modalDiv.append(data)
            $("#myModal").modal();

          }
        });
      });
      $(".deactivate").click(function () {

        var id = $(this).data(id);
        
        
        var csrftoken = '{{ csrf_token }}';
        $.ajax({
          type: "POST",
          url: "{% url 'user_inactive' %}",
          headers: { 'X-CSRFToken': csrftoken },
          data: id,
          
          success: function (data) {
            
          }
        });
        var is_active= $(this).data(is_active||'');
        console.log(is_active)
        var color=document.getElementById("deactive").style.color;
        if(is_active== "False")
              document.getElementById("deactive").style.color = "red";
        else
              document.getElementById("deactive").style.color = "green";
        
      });
      $('#table2').DataTable({
        buttons: [
          'excel'
        ],

        sDom: "lBfrtip",

      });
      $('#list1 li, #list2 li').on('click', function () {
          $(".dropdown").addClass('hover');
      });

    });