$(function() {

  // Set up the Highcharts graph.
  var chart = new Highcharts.Chart({
    chart: {
      renderTo: 'graph',
      zoomType: 'x'
    },
    title: {
      text: 'Temperatures by device:'
    },
    subtitle: {
      text: document.ontouchstart === undefined ? 'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
    },
    xAxis: {
      type: 'datetime',
      dateTimeLabelFormats: {
        minute: '%H:%M',
        hour: '%H:%M',
        day: '%b %e',
        week: '%b %e',
        month: '%b \'%y',
        year: '%Y'
      },
      min: new Date().getTime() - 7 * 24 * 60 * 60 * 1000,  // Default visible range of 1 week.
    },
    yAxis: {
      title: {
        text: 'Temperature (°F)'
      }
    },
    scrollbar: {
      enabled: true
    },
    tooltip: {
      formatter: function() {
        return Highcharts.dateFormat('%b %e %H:%M', this.x) + ': <strong>' + this.y + ' °F</strong>';
      }
    },
    plotOptions: {
      series: {
        marker: {
          radius: 1
        }
      }
    },
  });

  // Load a list of devices.
  $.getJSON('data/devices', function(devices) {

    // Iterate through the devices...
    $.each(devices, function(index, device) {

      // Load the device data.
      $.getJSON('data/device/' + device, function(data) {

        // Add it as a series to the chart.
        var series = {
          name: device,
          data: data
        }
        chart.addSeries(series);

        // Redraw.
        chart.redraw();
      });
    });
  });
});