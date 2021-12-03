var player;
var viedo_list;

    document.onreadystatechange = function(){
        if (document.readyState == 'interactive'){
            player = document.getElementById('player')
            viedo_list = document.getElementById('viedo_list')
            maintain_ratio()
           
            
        }
    }

    function maintain_ratio(){
        var w = player.clientWidth
        var h = (w*9)/16
        player.height = h
        viedo_list.style.maxHeight = h+'px'
    }
    window.onresize = maintain_ratio