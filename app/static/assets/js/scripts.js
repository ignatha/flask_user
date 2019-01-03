
var pendudukTable = $('#data-penduduk').DataTable({
        processing: true,
        serverSide: true,
        ajax: '/admin/fetchPenduduk',
        columns: [
            { data: 'DT_Row_Index', name: 'DT_Row_Index',orderable: false, searchable: false },
            { data: 'nik', name: 'nik' },
            { data: 'nama', name: 'nama' },
            { data: 'alamat', name: 'alamat' },
            { data: 'nomer_telepon', name: 'nomer_telepon' },
            { data: 'status_ktp', name: 'status_ktp' },
            { data: 'action', name: 'action',orderable: false, searchable: false }

        ]
    });

    $("#data-penduduk").css("width","100%");


 $(document).on('submit', 'form#form-edit-penduduk', function (event) {
    event.preventDefault();
    var form = $(this);
    var data = new FormData($(this)[0]);
    var url = form.attr("action");
    $.ajax({
        type: form.attr('method'),
        url: url,
        data: data,
        cache: false,
        contentType: false,
        processData: false,
        success: function (data) {
            $('.is-invalid').removeClass('is-invalid');
                if (data.fail) {
                     status = "<div class='alert alert-danger'><ul>";
                    for (control in data.errors) {
                        status += "<li>"+data.errors[control]+"</li>";
                    }
                    status += "</ul></div>";
                    $("#status-edit").html(status);
            } else {
                $('#edit-modal').modal('hide');
                pendudukTable.draw();
            }
        },
        error: function (xhr, textStatus, errorThrown) {
            alert("Error: " + errorThrown);
        }
    });
    return false;
});



function ajaxPendudukDelete(filename, token, content) {
    content = typeof content !== 'undefined' ? content : 'content';
    pendudukTable.draw();
    $.ajax({
        type: 'POST',
        data: {_method: 'DELETE', _token: token},
        url: filename,
        success: function (data) {
            $('#modalDelete-penduduk').modal('hide');
            $("#" + content).html(data);
            pendudukTable.draw();
        },
        error: function (xhr, status, error) {
            alert(xhr.responseText);
        }
    });
}

 $('#modalDelete-penduduk').on('show.bs.modal', function (event) {
      var button = $(event.relatedTarget);
      $('#penduduk_delete_id').val(button.data('id'));
      $('#penduduk_delete_token').val(button.data('token'));
  });

 $('#modalAktifKtp-penduduk').on('show.bs.modal', function (event) {
      var button = $(event.relatedTarget);
      $('#penduduk_aktif_id').val(button.data('id'));
      $('#penduduk_aktif_token').val(button.data('token'));
      $.ajax({
            url:"/admin/fetchDataPenduduk/"+button.data('id'),
            method:'get',
            dataType:'json',
            success:function(data)
            {
                $('#aktif-ktp-nik').val(data[0].nik);
                $('#aktif-ktp-nama').val(data[0].nama);
                $('#aktif-ktp-nomer_telepon').val(data[0].nomer_telepon);
            }
      });
  });

 function ajaxPendudukAktifKtp(filename, token, content)
 {
  content = typeof content !== 'undefined' ? content : 'content';
    pendudukTable.draw();
    $.ajax({
        type: 'POST',
        data: {_method: 'POST', _token: token},
        url: filename,
        success: function (data) {
            $('#modalAktifKtp-penduduk').modal('hide');
            pendudukTable.draw();
        },
        error: function (xhr, status, error) {
            alert(xhr.responseText);
        }
    });
 }

 $('body').on('hidden.bs.modal', '#show-modal', function () {
        $(this).removeData('bs.modal');
    });
 $('body').on('hidden.bs.modal', '#modal-penduduk', function () {
        $(this).removeData('bs.modal');
    });
 $('body').on('hidden.bs.modal', '#edit-modal', function () {
        $(this).removeData('bs.modal');
    });

 $('#modal-penduduk').on('show.bs.modal', function (event) {
        
});
