var columns = ["测点", "单位","运行数据"];

var tagtable = d3.select("#tagtable").append("table")
               .attr("class","table table-striped")
                          
var thead = tagtable.append("thead");
var tbody = tagtable.append("tbody")
       
//Add the header
thead.append("tr")
    .selectAll("th")
    .data(columns.slice(0, columns.length)) 
    .enter()
    .append("th")
    .attr("class", "row_title")
    .text(function (d) { return d; })

//Add the rows
var rows = tbody.selectAll("tr")
    .data(tabletaglist)
    .enter()
    .append("tr")
    .attr("class","row_tag");

var cells = rows.selectAll("td")
    .data(function (d) { return [d.tagdesc,d.tagunit,d.value]; })
    .enter()
    .append("td")
    .attr("class","cell_tag")
    .text(function(d) { return d; });
    
   