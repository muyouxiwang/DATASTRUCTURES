(ns control
  (:import (java.util.regex Pattern)
           (java.util Properties)
           (com.jcraft.jsch JSch Session))
  (:require [clojure.string :as string]
            [clojure.java.io :as io] 
            ))

;; (declare *jsch* *jsch-config* *jsch-session*)

(def ^:dynamic *jsch-session*)

(def ^:dynamic *jsch* (new com.jcraft.jsch.JSch))

(def ^:dynamic *jsch-config* (doto (new java.util.Properties)
                     (.put "StrictHostKeyChecking" "no")))

(defmacro with-session-with-port [user password host port & body]
  "This macro creates a ssh session that is valid within it's scope."
  `(binding [*jsch-session* (doto (.getSession *jsch* ~user ~host ~port)
                         (.setConfig *jsch-config*)
                         (.setPassword ~password)
                         ;; (.setTimeout 600)
                         (.connect))]
     (try
       (do ~@body)
       (finally (.disconnect *jsch-session*)))))



(defmacro with-session [user password host & body]
  "This macro creates a ssh session that is valid within it's scope, using the
default port 22 to connect."
  `(with-session-with-port ~user ~password ~host 22 ~@body))

(defn exec
  "Executes a command on the remote host and returns a seq of the lines the
  command retured."
  [command]
  (let
      [channel (.openChannel *jsch-session* "exec")]
    (doto channel
      (.setCommand command)
      (.setInputStream nil)
      (.setErrStream System/err))
    (with-open
      [stream (.getInputStream channel)]
      (.connect channel)
      (print (string/join "\n" (line-seq (io/reader stream)))))))



(with-session-with-port "root" "123456" "192.168.1.64" 3333
  (exec "su - muyouxiwang")
  (exec "ls")
  ;; (exec "df -h")
  )

(defn issubstr [s su]
  (not (= (.indexOf s su) -1)))

(defn hs2ms2qq [h3xml trans_type] 
  (let [moneytype  "<item key='moneytype' value='1'"
        new_moneytype  "<item key='moneytype' value='0'"
        minmoney  "<item key='minmoney' value="
        minmoney_end  "'/>"
        award  "<award key='"
        award_end  "'>"] 
    (cond
      (= trans_type "hs2ms")
      (map #(cond
              (issubstr % moneytype) (string/replace % moneytype new_moneytype)
              (issubstr % minmoney) (let [index (.indexOf % minmoney_end)]
                                      (str (.substring % 0 index) "0" (.substring % index)))
              (issubstr % award) (let [index (.indexOf % award_end)]
                                   (str (.substring % 0 index) "0" (.substring % index)))
              :else %) h3xml)
      (= trans_type "hs2qq")
      (map #(cond
              (issubstr % moneytype) (string/replace % moneytype new_moneytype)
              (issubstr % minmoney) (let [index (.indexOf % minmoney_end)]
                                      (str (.substring % 0 index) "00" (.substring % index)))
              (issubstr % award) (let [index (.indexOf % award_end)]
                                   (str (.substring % 0 index) "00" (.substring % index)))
              :else %) h3xml))))



(defn prop_source [filename]
  (with-open [rf (io/reader filename)]
    (reduce conj [] (map
                     #(string/split (string/trim %) #"###")
                     (filter
                      #(not (empty? (string/trim %)))
                      (line-seq rf))))))

(defn  make_props
  [prop_separators propnum_separators props]
  (let* [search_result  []
         prop_separators
         (string/split prop_separators #"|")
         propnum_separators
         (string/split propnum_separators #"|")
         prop_seq (first (filter
                          #(> (.indexOf props %) -1)
                          prop_separators))
         prop_lst (if (nil? prop_seq)
                    [props]
                    (string/split
                     props
                     (Pattern/compile
                      prop_seq)))]
    (defn one-item-results [search_name num]
      (filter #(not (nil? %))
              (map #(let [[pname prop_str] %]
                      (if (not (= (.indexOf pname search_name) -1))
                        (if (not (= (.indexOf prop_str "%d") -1))
                          (format prop_str num)
                          prop_str)))
                   (prop_source "./sourcefile.xml"))))

    (defn search-result [item]
      (reduce into []
              (map #(if (not (= (.indexOf item %) -1))
                      (let [[search_name num]
                            (string/split item
                                       (Pattern/compile %))]
                        (one-item-results
                         search_name (Integer/parseInt num))))
                   propnum_separators)))

    (reduce into [] 
            (map #(if (= (count %) 0) "????----" %)
                 (map search-result prop_lst)))))




(defn main []

  ;; (print (prop_source "./sourcefile.xml"))
  (print (make_props "，|、|," "*|×|x"
    "宝石25×15，紅鑽石30×2，藍鑽石30×8，黃鑽石30×6，未知30×4，未知30+6")))

;; (print (issubstr "abcdefg" "def"))
;; (print (issubstr "abcdefg" "uil"))

;; (with-open [rf (io/reader "大部分运营商（幻三）  1月26日（充值送好礼）.xml")]
;;   (let [content (string/join "\n" (hs2ms2qq (line-seq rf) "hs2ms"))]
;;     (spit "result_ms.xml" content)))
;; (with-open [rf (io/reader "大部分运营商（幻三）  1月26日（充值送好礼）.xml")]
;;   (let [content (string/join "\n" (hs2ms2qq (line-seq rf) "hs2qq"))]
;;     (spit "result_qq.xml" content)))



;; java -cp ./;clojure-1.8.0.jar;jsch-0.1.54.jar clojure.main control.clj




