nmlst = ["Kanbaru","Hitagi","Tsukihi","Karen"]
race1 = [11,30,60,35]
race2 = [50,11,10,7]

meow = zip.race1.race2

calcu: (Int,Int) -> Int
calcu.(x,y) = (x+y)/2

aver: [Int]
aver = [calcu.(e,f)|(e,f) <- meow]
 

felix: [Int] -> Int
felix.[] = 0
felix.(x::xs) = if (x>y) then x else y
                  where 
                     y = felix.xs

subaru: [Int] -> Int
subaru.[] = 0
subaru.[x] = x
subaru.(x::xs) = if (x<y) then x else y
                   where
                     y=subaru.xs

mew2 = zip.nmlst.aver

winner: [[Char]]
winner = [m|n=felix.aver, (m,n) <- mew2]