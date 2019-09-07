function audioPlayer() {

    var currentSong = 0;
    $("#audioPlayer")[0].src = $("#playlist td a")[0];
    $("#audioPlayer")[0].play();
    $("#playlist td a").click(function(e){
       e.preventDefault();
       $("#audioPlayer")[0].src = this;
       $("#audioPlayer")[0].play();
        currentSong = this.parentNode.parentNode.rowIndex;
        currentSong = currentSong*2;
    });

    $("#audioPlayer")[0].addEventListener("ended", function(){
        currentSong+=2;
        $("#audioPlayer")[0].src = $("#playlist td a")[currentSong];
        $("#audioPlayer")[0].play();
    });
}