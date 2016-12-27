fun getListLength([]) = 0
	|	getListLength(Y::Ys) = if Ys=[] then 1
							   else 1 + getListLength(Ys);

fun member(X,L) = 	if L=[] then false
      				else if X=hd(L) then true
      				else member(X,tl(L));

fun remove(x,L) = 	if (L=[]) then []
         			else if x=hd(L)then remove(x,tl(L))
         			else hd(L)::remove(x,tl(L));

fun reverse(L)	= 	if L = [] then []
					else reverse(tl(L))@ [hd(L)];
						
fun stageList(N)=	if N = 0 then []
					else (N-1)::stageList(N-1);


fun reList_helper(C,Ls)	= 	if hd(Ls) = C then Ls
							else reList_helper(C, tl(Ls) @ [hd(Ls)]);

fun reList(C,N) = reList_helper(C,reverse(stageList(N)));

fun reListC(C,N) = reList_helper(C,stageList(N));


fun findStage(N,SL)= 	if N = 1 then hd(SL)
						else findStage(N-1,tl(SL));

fun minus([],L2) = []
	| minus(L1,[]) = L1 
	| minus(X::Xs,L2) = if member(X,L2) then minus(Xs,L2)
             			else X::minus(Xs,L2);

fun union(L1,L2) = 	if L1=[] then L2
					else if member(hd(L1),L2) then union(tl(L1),L2)
					else hd(L1)::union(tl(L1),L2)

fun equal(L1,L2) = 	if L1 = [] andalso L2 = [] then true
					else if L1 = [] orelse L2 = [] then false
					else if member(hd(L1),L2) then equal(remove(hd(L1),L1),remove(hd(L1),L2))
					else false;

fun findFL(S,[])	=	[]
	|	findFL(S,St::Ss)=	if hd(hd(St)) = S then hd(tl(St))
							else findFL(S,Ss);
					
fun setStage_helper(0) = []
	| 	setStage_helper(n) = [[n-1],[n-1]]::setStage_helper(n-1);


fun setStage(n)	=	if n = 0 then []
					else reverse(setStage_helper(n));

fun findConnected(n,[]) = []
	|	findConnected(n,St::Ss) = if member(n,hd(tl(St))) then
												if n = hd(hd(St)) then findConnected(n,Ss)
												else hd(hd(St))::findConnected(n,Ss)
											else findConnected(n,Ss);

fun addConnected([],L) = []
	|	addConnected(St::Ss,L) =  
							[hd(St), union(hd(tl(St)),findConnected(hd(hd(St)),L))]::addConnected(Ss,L);

fun pro0_helper([],S,H) = []
	| 	pro0_helper(St::Ss,S,H) = 	if hd(hd(St)) = S then [hd(St), union(hd(tl(St)),[H])]::Ss			
									else St::pro0_helper(Ss,S,H);

fun pro0(SL,S,H) = 	if SL = [] then []
					else addConnected(pro0_helper(SL,S,H),pro0_helper(SL,S,H));


fun pro1_helper([],S,H,SL) = []
	|	pro1_helper(St::Ss,S,H,SL) = 	if hd(hd(St)) = S then [hd(St), remove(H,union(hd(tl(St)),findFL(H,SL)))]::Ss
										else St::pro1_helper(Ss,S,H,SL);

fun pro1(SL,S,H) = 	if SL = [] then []
					else addConnected(pro1_helper(SL,S,H,SL),pro1_helper(SL,S,H,SL));

fun pro2_helper([],S,H,SL) = []
	|	pro2_helper(St::Ss,S,H,SL) = 	if hd(hd(St)) = S then [hd(St), union(hd(tl(St)),findFL(H,SL))]::Ss
										else St::pro2_helper(Ss,S,H,SL);

fun pro2(SL,S,H) = 	if SL = [] then []
					else addConnected(pro2_helper(SL,S,H,SL),pro2_helper(SL,S,H,SL));

fun process(SL,(S,H,P))	= 	if P = 0 then pro0(SL,S,H)
							else if P = 1 then pro1(SL,S,H)
							else if P = 2 then pro2(SL,S,H)
							else SL;

fun finalProcess_helper(SL,LIP)	= 	if LIP = [] then SL
									else process(finalProcess_helper(SL,tl(LIP)),hd(LIP));

fun finalProcess(SL,LIP) = 	if LIP = [] then SL 
							else finalProcess_helper(SL,reverse(LIP));


fun findPair_helper(C, N,SL,Ls) = 
	if N = hd(reverse(Ls)) then Ls
	else if C+1 > getListLength(minus(Ls,remove(N,findFL(N,SL))))  then minus(Ls,remove(N,findFL(N,SL)))
	else findPair_helper(C+1,findStage(C+1,minus(Ls,remove(N,findFL(N,SL)))), SL, minus(Ls,remove(N,findFL(N,SL))));

fun findPair(C,SL,N) = 	if C = 0 then []
						else findPair_helper(1,C-1,SL,reList(C-1,N))::findPair(C-1,SL,N);

fun findPairC(C,SL,N) = if C = 0 then []
						else findPair_helper(1,C-1,SL,reListC(C-1,N))::findPairC(C-1,SL,N);


fun getPair(N,SL)=	if SL = [] orelse N = 0 then []
					else findPair(N,finalProcess(setStage(N),SL),N) @ findPairC(N,finalProcess(setStage(N),SL),N);


fun getConfidence(Ps,Cs,Sum) = 	if Ps = [] then Sum
								else getConfidence(tl(Ps),Cs,Sum+findStage(hd(Ps)+1,Cs));

fun getConfidenceList_helper(PLs,Cs) = if PLs = [] then []
								else getConfidence(hd(PLs),Cs,0)::getConfidenceList_helper(tl(PLs),Cs);

fun getConfidenceList(N,SL,Cs)= if N = 0 then []
								else if SL = [] then []
								else if Cs = [] then []
								else getConfidenceList_helper(getPair(N,SL),Cs);

fun getMax(L,M) = 	if L = [] then M
					else if hd(L) > M then getMax(tl(L),hd(L))
					else getMax(tl(L),M);

fun survey(N,SL,Cs)= if N = 0 then 0 
					 else if SL = [] orelse Cs = [] then 0
					 else getMax(getConfidenceList(N,SL,Cs),0);





