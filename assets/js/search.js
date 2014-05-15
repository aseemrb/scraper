function showElements(response) {
    document.getElementById('response').innerHTML = "";
    document.getElementById('response').innerHTML += "<div class='row-fluid'>";
	for(var i=0;i<response.anchors.length;i++)
    {
        var snipobj = response.anchors[i];
        if(i%8==0)
            document.getElementById('response').innerHTML += "</div><br><div class='row-fluid'>";
        document.getElementById('response').innerHTML += 
                "<div class='span2'>" +
                    "<a href='"+snipobj.hlink+"'>" + snipobj.hlink.split('/')[3].charAt(0).toUpperCase() + 
                    snipobj.hlink.split('/')[3].slice(1) + "</a>" +
                "</div>";
    }
    document.getElementById('response').innerHTML += '<br><br>';
}

function showImages(response) {
	document.getElementById('response').innerHTML = "";
    document.getElementById('response').innerHTML += "<div class='row-fluid'>";
    for(var i=0;i<response.urls.length;i++)
    {
        var snipobj = response.urls[i];
        if(i%4==0)
            document.getElementById('response').innerHTML += "</div><br><br><div class='row-fluid'>";
        document.getElementById('response').innerHTML +=
                    "<div class='span4'>" +
        				"<img src='"+snipobj.url+"'>" +
        			"</div>";
    }
    document.getElementById('response').innerHTML += '<br><br>';
}

function elems() {
    var xhr = new XMLHttpRequest();
    var url = document.getElementById('query').value;    
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4)
        	showElements(JSON.parse(xhr.responseText));
    }
    xhr.open("GET", "scrape/?url=http://www.webelements.com/", false);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send();
}

function search() {
    var xhr = new XMLHttpRequest();
    var url = document.getElementById('query').value;    
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4)
        	showImages(JSON.parse(xhr.responseText));
    }
    xhr.open("GET", "scrape/?url=" + url, false);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send();
    xmlDocument = xhr.responseText;
}