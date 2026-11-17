# GAP 4 script reconstructed from explicit generators in original manuscript.
# Run: gap -q scripts/verify_generators.g
cases := [
 rec(n:=10,k:=3,ord:=720,gens:=[(2,6,10,7)(3,9,4,5),(1,5)(3,8)(4,10)(7,9)]),
 rec(n:=11,k:=4,ord:=7920,gens:=[(1,2,3,4,5,6,7,8,9,10,11),(3,7,11,8)(4,10,5,6)]),
 rec(n:=12,k:=5,ord:=95040,gens:=[(2,3,5,9,8,10,6,11,4,7,12),(1,12)(2,11)(3,10)(4,9)(5,8)(6,7)])
];
for c in cases do
  G:=Group(c.gens);
  tup:=[1..c.k];
  orb:=Orbit(G,tup,OnTuples);
  Print("n=",c.n," order=",Size(G)," orbit=",Length(orb),"\n");
  if Size(G)<>c.ord or Length(orb)<>c.ord then Error("verification failed"); fi;
od;
Print("All original generators verified.\n");
