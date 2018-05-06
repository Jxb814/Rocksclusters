/*

Author:   Cheng Maohua
Email:    cmh@seu.edu.cn

License: this code is in the public domain
*/

ws.onmessage = function(evt) {
     	
	    var msg = evt.data;
    
     	var objresponse = JSON.parse(msg);
 	    var tagcount=objresponse['value'].length;
 	    
 	    for (var i = 0; i <tagcount; i++) 
 	    {
 	    	tabletaglist[i].value=objresponse['value'][i].toFixed(2);
 	    }           	   
 	    
 	   var vis = d3.select("#tag").selectAll(".taglabel")
	    .data(tabletaglist)
	    .text(function(d) { return d.tagdesc+": "+d.value+" "+d.tagunit; });
 	    
 	                    
};
 	 
ws.onopen = function() {
 	   ws.send("Open New Client");
};

