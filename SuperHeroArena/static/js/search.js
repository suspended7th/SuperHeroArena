function ChangeSearchType(value){
    if(value=="name"){
        document.getElementById('namerow').style.display='';
        document.getElementById('simpleregexrow').style.display='none';
        document.getElementById('regexrow').style.display='none';
    }else if(value=="simple_regex"){
        document.getElementById('namerow').style.display='none';
        document.getElementById('simpleregexrow').style.display='';
        document.getElementById('regexrow').style.display='none';
    }else if(value=="regex"){
        document.getElementById('namerow').style.display='none';
        document.getElementById('simpleregexrow').style.display='none';
        document.getElementById('regexrow').style.display='';
    }
}

window.onload = function() {
	ChangeSearchType(document.getElementById('search_type').value);
}