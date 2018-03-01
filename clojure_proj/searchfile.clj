(ns searchfile
  (:require [clojure.string :as str]
             [clojure.java.io :as io]))


(def root-dir "E:/test/source_code/server")


(defn first-pro []
  (println root-dir))




(defn is-legal-file [filename exts]
  (exts (last (str/split filename #"\."))))

(defn enumerate [lst]
  (map #(conj [%1 %2]) (range (count lst)) lst))



(defn search-file [f exts pattern]
  (if (is-legal-file (.getName f) exts)
    (with-open [rf (io/reader f)]
      (doall (filter #(re-find pattern (% 1))
                     (enumerate (line-seq rf)))))))


(defn search-dir [dir exts pattern]
  #_(let [search-result []]
    (doseq [f (file-seq (io/file dir))]
        ;; (print f)
        ;; (into search-result (search-file f exts pattern))
        #_(if (directory? f)
            (into search-result (search-dir f exts pattern))
            (into search-result (search-file f exts pattern)))
        (if (.isFile f)
            (dorun (into search-result (search-file f exts pattern))))))
    #_(doall (map #(into search-result (search-file % exts pattern))
                (rest (file-seq (io/file dir)))))
  (reduce into [] (map #(if (.isFile %)
                          (search-file % exts pattern))
                       (file-seq (io/file dir)))))

(defn main []
  ;; (first-pro)
  ;; (if (is-legal-file "shit.py")
  ;; (println "py"))
  ;; (if (is-legal-file "shit.lisp")
  ;; (println "lisp"))
  (print (search-dir root-dir #{"py" "lisp" "html" "ini"} #"on_user_info"))
  ;; (print (search-dir root-dir #{"py" "lisp" "html" "ini"} #"__init__"))
  ;; (print (search-file "./war.py" nil #"__init__"))
  )

;; java -cp clojure-1.8.0.jar clojure.main searchfile.clj



