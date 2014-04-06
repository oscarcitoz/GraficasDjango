var b;
            var chart;
			var t=[];
			var total3=[];
		 	var total=[];
			var total2=[];
            $(document).ready(iniciar);
function iniciar()
{		
	$("table#1").hide();
	$("table#1 tr:first").css("font-weight","bold");
	$("div#0").css("cursor","pointer");
	$("table#1 tr:last").css("font-weight","bold");
	$("table#1 tr:even").css("background-color","#CEEFFF");
	$("div#0").click(function()
	{	if($("table#1").is (':hidden')){
		$("table#1").show();
		$("div#0 h1").text("Presiona para ocultar la tabla");}
		else{
		$("table#1").hide();
		$("div#0 h1").text("Presiona para ver la tabla");
		}
	});	
	$("div#2").click(function(){
					$("td#Periodo").each(function(i,valor) {
                      total[i]=parseFloat($(this).text());
                   });	
				   $("td#fecha").each(function(i,valor) {
                      total2[i]=parseFloat($(this).text());
                   });
				   $("td#y").each(function(i,valor) {
                      total3[i]=parseFloat($(this).text());
                   });
				  
				$.each(total,function(i){
					 t[i]=[total[i],total3[i]];
					 });
				   x=total[2];
				   alert(x);
                chart = new Highcharts.Chart({
                    chart: {renderTo: 'container',},
                    title: {text: 'Grafica'},
                    xAxis: {title:{ text: 'Periodo'} },  
        			yAxis: {
						title:{text:'precio'}},  
					/*tooltip: {
                        formatter: function() {
                            return '<b>'+ this.point.name +'</b>: '+ this.y +' %';
                        }
                    
                    plotOptions: {
                        pie: {
                            allowPointSelect: true,
                            cursor: 'pointer',
                            dataLabels: {
                                enabled: false
                            },
                            showInLegend: true
                        }
                    },*/
               series: [{
				   pointInterval:  1,  
      pointStart: total[0], 
            data: total2
         }, { 
      pointInterval:  1,  
      pointStart: total[0],  
      data:t
    }]  
  }); 
});
}