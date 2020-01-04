CAPTURE_IMG_WIDTH = 640
CAPTURE_IMG_HEIGHT = 480

jQuery.ajaxSetup({
  beforeSend: function() {
     $('#loading').removeClass('hidden');
  },
  complete: function(){
     $('#loading').addClass('hidden');
  },
  success: function() {
    $('#loading').addClass('hidden');
  }
});

// HTML5 WEBCAM
Webcam.set({
  width: CAPTURE_IMG_WIDTH,
  height: CAPTURE_IMG_HEIGHT,
  image_format: 'jpeg',
  jpeg_quality: 90
});
Webcam.attach( '#my-camera' );

let form_capture = document.getElementById('form-capture-image')
$('.btn-capture-image').on('click', function(e) {
  e.preventDefault();

  Webcam.snap(function(data_uri) {
    // display results in page
    // readURL(data_uri, '#input-data-uri')
    let json_data = {'data-uri': data_uri }

    $.ajax({
      type: 'POST',
      url: '/predict/',
      processData: false,
      contentType: 'application/json; charset=utf-8',
      dataType: 'json',
      data: JSON.stringify(json_data),
      success: function(data) {
        console.log(data)
        html = '<ul>'
        for( let i = 0; i < data['probs'].length; i++) {
          data_splitted = data['probs'][i]

          html += '<li><span class="num">' + data_splitted[0] + '</span> <span class="prob">'+ data_splitted[1] + '</span></li>'
        }
        html += '</ul>'

        $('#probs').text('').append(html)
        $('#class-result').text('Predictions: ' + data['label']);

        // $('.box-main').css('height', $('.box-results').height());
      }
    });
  });
});