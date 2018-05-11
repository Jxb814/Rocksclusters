var vis = d3.select("#tag").selectAll("label")
						      .data(tabletaglist)
						      .enter()
						      .append("label")
						      .attr("class", "taglabel")
					          .attr("font-size", "24px")
						      .style("color","black")
						      .text(function(d) { return  d.tagdesc+": "+d.value+" "+d.tagunit; });
