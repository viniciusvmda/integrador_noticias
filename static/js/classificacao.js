function associarMateria(element) {
    var linha = $(element).closest('tr');
    var materia_id = $(linha).find("#classificacao-materia-id").text();
    var caderno_id = $(linha).find('#sel-caderno').val();
    data = {
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        materia_id: materia_id,
        caderno_id: caderno_id,
    }
    $.ajax({
      type: "POST",
      url: '/classificacao/',
      data: data,
      complete: function(r){
       $("body").html(r.responseText);
      },
      dataType: 'json'
    });
}