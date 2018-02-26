
(ns test
  (:require [control :refer :all]))




#_(defn test-count-sub []
  (and (= (count-sub "abcdefg" "cde") 1)
       (= (count-sub "abcdesklcdelslcdefg" "cde") 3)
       (= (count-sub "sldfl" "ooo") 0)))



(defn report-result [result form]
  (print (str (if result "[pass] " "[FAIL~] ") form "\n"))
  result)



(defmacro combine-results [& forms]
  `(let [ret# (atom true)]
     (do ~@(for [form forms]
             `(if-not ~form (reset! ret# false))))
     '@ret#))

#_(print (macroexpand '(combine-results (true? true)
                                      (false? true))))

(print (combine-results (true? true)
                 (false? true)))

(defmacro add-print [form]
  `(print ~form))

(defmacro make-li [& forms]
  `(do ~@(for [form forms] `(print ~form))))


;; (print (macroexpand '(make-li (print "shit") (print "fuck") (print "crap"))))

;; (print (macroexpand '(add-print "it is fuckup")))
;; (print (macroexpand '(make-li "shit" "fuck" "crap")))
;; (make-li "shit" "fuck" "crap")



#_(defmacro check [form]
  `(report-result ~form '~form))

(defmacro check [& forms]
  `(combine-results ~@(for [form forms] `(report-result ~form '~form))))

#_(defn test-count-sub []
  (report-result (= (count-sub "abcdefg" "cde") 2) '(= (count-sub "abcdefg" "cde") 1))
  (report-result (= (count-sub "abcdesklcdelslcdefg" "cde") 3)
                 '(= (count-sub "abcdesklcdelslcdefg" "cde") 3))
  (report-result (= (count-sub "sldfl" "ooo") 0) '(= (count-sub "sldfl" "ooo") 0)))

#_(defn test-count-sub []
  (check (= (count-sub "abcdefg" "cde") 2))
  (check (= (count-sub "abcdesklcdelslcdefg" "cde") 3))
  (check (= (count-sub "sldfl" "ooo") 0)))

#_(defn test-count-sub []
  (check
   (= (count-sub "abcdefg" "cde") 2)
   (= (count-sub "abcdesklcdelslcdefg" "cde") 3)
   (= (count-sub "sldfl" "ooo") 0)))


#_(print (macroexpand '(check
   (= (count-sub "abcdefg" "cde") 2)
   (= (count-sub "abcdesklcdelslcdefg" "cde") 3)
   (= (count-sub "sldfl" "ooo") 0))))
;; (test-count-sub)








#_(defn test-issubstr []
  (and (true? (issubstr "abcdefg" "bcd"))
       (true? (issubstr "ooxlsdfs" "lsd"))
       (false? (issubstr "lllll" "aaaa"))))

#_(test-issubstr)



;; java -cp ./;clojure-1.8.0.jar;jsch-0.1.54.jar clojure.main test.clj
