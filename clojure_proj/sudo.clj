(ns sudo
  (:require [clojure.set :as set]))




(def b2 '[3 - - - - 5 - 1 -
          - 7 - - - 6 - 3 - 
          1 - - - 9 - - - - 
          7 - 8 - - - - 9 - 
          9 - - 4 - 8 - - 2 
          - 6 - - - - 5 - 1 
          - - - - 4 - - - 6 
          - 4 - 7 - - - 2 - 
          - 2 - 6 - - - - 3])

(def b3 '[2 - 8 - - - - 9 - 
          5 6 3 - - 1 - 4 7 
          7 4 - - - 5 1 2 6 
          - - - 5 - - 6 3 9 
          9 - - 1 4 3 - - 8 
          3 - 7 6 9 - 5 1 4 
          - 7 1 3 8 9 - - 2 
          4 - 5 2 1 6 - 8 3 
          8 3 2 - - 7 9 6 1])

(def b4 '[- 4 - - - 8 5 - - 
          1 - - - - 9 - - 6 
          5 - - 1 7 4 - - - 
          - 7 - 3 4 - - 9 - 
          - - 5 - - 2 4 - - 
          6 - 4 - 1 - 8 - 2 
          - - - - - - 2 - - 
          4 - - - 2 7 - - 1 
          8 2 - 4 - - - 3 - ])

#_(def b1 '[1  2  3  4  5  6  7  8  9
          10 11 12 13 14 15 16 17 18
          19 20 21 22 23 24 25 26 27
          28 29 30 31 32 33 34 35 36
          37 38 39 40 41 42 43 44 45
          46 47 48 49 50 51 52 53 54
          55 56 57 58 59 60 61 62 63
          64 65 66 67 68 69 70 71 72
          73 74 75 76 77 78 79 80 81])

(defn prep [board]
  (map #(partition 3 %)
       (partition 9 board)))


(defn print-board [board]
  (let [row-sep (apply str (repeat 37 "-"))] 
    (println row-sep) 
    (dotimes [row (count board)] 
      (print "| ") 
      (doseq [subrow (nth board row)] 
        (doseq [cell (butlast subrow)] 
          (print (str cell "         "))) 
        (print (str (last subrow) " | "))) 
      (println) 
      (when (zero? (mod (inc row) 3)) 
        (println row-sep))))) 

(defn rows [board sz] 
  (partition sz board)) 

(defn row-for [board index sz] 
  (nth (rows board sz) (/ index 9))) 

(defn column-for [board index sz] 
  (let [col (mod index sz)] 
    (map #(nth % col)
         (rows board sz))))

(defn subgrid-for [board i] 
  (let [rows (rows board 9)                    
        sgcol (/ (mod i 9) 3)
        sgrow (/ (/ i 9) 3)                   
        grp-col
        (column-for (mapcat #(partition 3 %) rows) sgcol 3)  
        grp (take 3 (drop (* 3 (int sgrow)) grp-col))]
    (flatten grp)))  


(defn numbers-present-for [board i] 
  (set 
   (concat (row-for board i 9) 
           (column-for board i 9) 
           (subgrid-for board i))))

(defn possible-placements [board index]
  (set/difference #{1 2 3 4 5 6 7 8 9}
                  (numbers-present-for board index)))

(defn index [coll]
  (cond
    (map? coll) (seq coll)
    (set? coll) (map vector coll coll)
    :else (map vector (iterate inc 0) coll)))



(defn pos [pred coll]
  (for [[i v] (index coll) :when (pred v)] i))

(defn solve [board]
  (if-let [[i & _]                                     
           (and (some '#{-} board)
                (pos '#{-} board))]
    (flatten (map #(solve (assoc board i %))          
                  (possible-placements board i))) 
    board))                                           

(-> b4
    solve
    prep
    print-board)






