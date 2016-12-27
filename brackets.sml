fun finalized(E,L) 	= 	if L = [] then []
						else if hd(L) = 0 then E+1::finalized(E+1,tl(L))
						else E-1::finalized(E-1,tl(L));

fun getListMax([]) = 0
	|   getListMax(Y::Ys) = if Ys = [] then Y
						  	else if Y > hd(Ys) then getListMax(Y::tl(Ys))
							else getListMax(Ys);

fun getListLength([]) = 0
	|	getListLength(Y::Ys) = if Ys=[] then 1
							   else 1 + getListLength(Ys);

fun splitList_prefix([]) = []
	|	splitList_prefix(X::Xs) = 	if X = 0 then [0]
									else X::splitList_prefix(Xs);

fun splitList_delete_prefix([]) = []
	|	splitList_delete_prefix(X::Xs) 	= 	if X = 0 then Xs
		 								 	else splitList_delete_prefix(Xs);
											

fun splitList(L) = 	if L = [] then []
					else (hd(L)::splitList_prefix(tl(L)))::splitList(splitList_delete_prefix(tl(L)));


fun reduceLevel_helper([]) = []
	|	reduceLevel_helper(X::Xs) = if Xs = [] then []
									else X - 1::reduceLevel_helper(Xs);

fun reduceLevel(L) 	= 	if L = [] then []
					 	else reduceLevel_helper(tl(L));



fun getOutArea(L) 	= 	if L = [] then 0
						else getListMax(L) * (getListLength(L) - 1);


fun	getEvenCase(O,[]) = 0
	|	getEvenCase(O,X::Xs)	= 	if O = ~1 then	
										(0 - getOutArea(X)) + getEvenCase(1,splitList(reduceLevel(X))) + getEvenCase(~1,Xs)
									else	
										getOutArea(X) + getEvenCase(~1,splitList(reduceLevel(X))) + getEvenCase(1,Xs);

fun brackets_helper([]) = 0
	|	brackets_helper(X::Xs) 	= 	(0 - getEvenCase(~1,[X]) + brackets_helper(Xs));

fun brackets(L) = 	if L = [] then 0
					else brackets_helper(splitList(finalized(0,L)));

						 