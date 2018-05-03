ws.onmessage = function(evt) {
     	var msg = evt.data;
    
     	var objresponse = JSON.parse(msg);
 	    var tagcount=objresponse['value'].length;
 	    
 	    tabi=0;
 	    figi=0;
 	    for (var i = 0; i <tagcount; i++) 
 	    {
 	        taglist[i].value=objresponse['value'][i].toFixed(2);
 	       
 	        if (taglist[i].tab==1.0)
 	        {
 	           tabletaglist[tabi].value=taglist[i].value;
 	           tabi=tabi+1;
 	       	 }
 	        
 	        if (taglist[i].fig==1.0)
	        {
	           figtaglist[figi].value=taglist[i].value;
	           figi=figi+1;
	        }
 	     }           	   
 	    
 	 	 var vis=d3.selectAll(".tagtext")
		     .data(figtaglist)
		     .text(function(d) { return d.value+d.tagunit; });
 	 	 
 		
  	    var vis = d3.select("#tag").selectAll(".taglabel")
  	           .data(tabletaglist)
  	           .text(function(d) { return d.tagdesc+": "+d.value+" "+d.tagunit; });
 	 	 
 	 	var tbody = d3.select("#tagtable").select(".table").select(".tbody");
 	 	var rows = tbody.selectAll(".row_tag")
 	 	           .data(tabletaglist);
 	 		    	
 	 	var cells = rows.selectAll(".cell_tag")
 	 	           .data(function(d) { return [d.tagdesc,d.tagunit,d.value]; })
 	 	    	   .text(function(d) { return d; });
	  	
	 	
 };   
 	 
ws.onopen = function() {
 	   ws.send("new Client ON");
};

