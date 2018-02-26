
(ns test
  (:require [control :refer :all]))



;; ==========================================================================================

(def ^:dynamic *test-name* "")


(defn report-result [result form]
  (print (str (if result "[SUCC] " "[FAIL~!!!] ") *test-name* form "\n"))
  result)

(defmacro combine-results [& forms]
  (let [ret (gensym)]
    `(let [~ret (atom true)]
       (do ~@(for [f# forms]
               `(if-not ~f#
                  (reset! ~ret false))))
       @~ret)))

(defmacro check [& forms]
  `(combine-results ~@(for [form forms]
                        `(report-result ~form '~form))))

(defmacro deftest [name args & body]
  `(defn ~name ~args
     (binding [*test-name* (str *test-name* ":" '~name)]
       ~@body)))

;; ==========================================================================================




(deftest test-count-sub []
  (check
   (= (count-sub "abcdefg" "cde") 1)
   (= (count-sub "abcdesklcdelslcdefg" "cde") 6)
   (= (count-sub "sldfl" "ooo") 0)))

(deftest test-issubstr []
  (check
   (true? (issubstr "abcdefg" "bcd"))
   (true? (issubstr "ooxlsdfs" "lsd"))
   (false? (issubstr "lllll" "aaaa"))))

(deftest test-model-control []
  (combine-results
   (test-count-sub)
   (test-issubstr)))


(println (test-model-control))













;; java -cp ./;clojure-1.8.0.jar;jsch-0.1.54.jar clojure.main test.clj
