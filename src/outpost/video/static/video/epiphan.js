$(document).ready(function() {
  $('#channels .channel').each(function(idx, elem) {
    var url = $(elem).data('url');
    var status = $(elem).find('.status');
    var start = $($.templates('#tmpl-channel-start').render());
    var stop = $($.templates('#tmpl-channel-stop').render());
    start.hide();
    stop.hide();
    status.append(start);
    status.append(stop);
    start.on('click', function() {
      start.prop('disabled', true);
      $.ajax(
        url,
        {
          method: 'START',
          dataType: 'json'
        }
      );
    });
    stop.on('click', function() {
      stop.prop('disabled', true);
      $.ajax(
        url,
        {
          method: 'STOP',
          dataType: 'json'
        }
      );
    });

    var refresh = function(){
      $.ajax(
        url,
        {
          method: 'GET',
          dataType: 'json'
        }
      ).done(function(data) {
        if (data.recording) {
          $(elem).addClass('success');
          start.hide();
          stop.show();
        } else {
          $(elem).removeClass('success');
          start.show();
          stop.hide();
        }
        start.prop('disabled', false);
        stop.prop('disabled', false);
      });
    };

    refresh();
    setInterval(refresh, 4000);
  });

  var $notification = $('#notification')
  $notification.on('click', function() {
    if ($notification.data('enabled') === 'true') {
      $notification.removeClass('btn-success').addClass('btn-default');
      $notification.find('span.glyphicon').removeClass('glyphicon-check').addClass('glyphicon-unchecked');
      $notification.data('enabled', 'false');
    } else {
      $notification.removeClass('btn-default').addClass('btn-success');
      $notification.find('span.glyphicon').removeClass('glyphicon-unchecked').addClass('glyphicon-check');
      $notification.data('enabled', 'true');
    }
  });
  if ($notification.data('enabled') === 'true') {
    $notification.addClass('btn-success');
    $notification.find('span.glyphicon').addClass('glyphicon-check');
  } else {
    $notification.addClass('btn-default');
    $notification.find('span.glyphicon').addClass('glyphicon-unchecked');
  }
  $notification.removeClass('hidden')

});
