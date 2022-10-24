function redirect() {
    let input = document.getElementById('number').value;
        window.location.href = '/square/' + input;
}


//function redirect() {
//    let input = document.getElementById('number').value;
//    if(typeof input === number){
//        window.location.href = '/square/' + input;
//    }else {
//        window.location.href = '/';
//    };
//}
