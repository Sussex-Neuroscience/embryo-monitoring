bpDiam=122;
bpHei = 4;
fibDiam=18;
fibHei=15;

$fn=100;
tol=0.1;


cylinder(d=bpDiam-2*tol,h=bpHei);




module fibreCoupler(){
    rotate([0,90,0]){
    difference(){
cylinder(d=fibDiam+4+2*tol,h=fibHei);
translate([0,0,1]){
    
cylinder(d=fibDiam+2*tol,h=fibHei+2);
  }//end translate
  translate([0,0,-1]){
    cylinder(d=fibDiam-2+2*tol,h=fibHei+2);
  }//end translate

}//end difference
//
}//end rotate

}//end module

translate([bpDiam/2-fibHei-5,10,14]){
fibreCoupler();
}//end translate

translate([-(bpDiam/2-fibHei-5),10,14]){
    rotate([0,0,180]){
fibreCoupler();
}//end translate
}