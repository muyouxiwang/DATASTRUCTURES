(ns control
  (:import (java.util.regex Pattern)
           (java.util Properties)
           (com.jcraft.jsch JSch Session ProxyHTTP))
  (:require [clojure.string :as string]
            [clojure.java.io :as io] 
            ))

(defn ssh-exec-cmds
  ([host port user password commands]
   (ssh-exec-cmds host port user password commands nil nil))

  ([host port user password commands proxyhost proxyport]
   (let* [jsch-config (doto (Properties.)
                        (.put "StrictHostKeyChecking" "no"))
          proxy (if (and proxyhost proxyport)
                  (ProxyHTTP. proxyhost proxyport))
          session (doto (let [-session (.getSession (JSch.) user host port)]
                          (doto -session
                            (.setConfig jsch-config)
                            (.setPassword password)
                            (.setTimeout 600))
                          (if proxy
                            (.setProxy -session proxy))
                          -session)
                    (.connect))
          channel (doto (.openChannel session "shell")
                    (.connect))
          buff (StringBuilder.)]
     (try
       (with-open
         [in (io/reader (.getInputStream channel))
          out (io/writer (.getOutputStream channel))]
         
         (defn shell-println [cmd]
           (.write out (str (string/trim cmd) "\n"))
           (.flush out))

         (defn shell-read-all []
           (while (or (.ready in) (Thread/sleep 1000) (.ready in))
             (.append buff (char (.read in)))))
         
         (shell-read-all)
         (doseq [cmd commands]
           (shell-println cmd)
           (shell-read-all))

         (.toString buff))
       (finally (.disconnect session))))))

#_(print (ssh-exec-cmds
        "192.168.1.64" 3333 "muyouxiwang" "123456" 
        ["ps aux"
         "ls"
         "df -h"]))

;; (print (ssh-exec-cmds
;;         "sgtest.198game.com" 63572 "youease" "3841c3847a98da37da83a212a8d4c14e" 
;;         ["sudo su - sislcb"
;;          "ls"] "125.90.93.53" 36000))

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


(def make_props
  (let [prop_source
        (with-open [rf (io/reader "./sourcefile.xml")]
          (reduce conj [] (map
                           #(string/split (string/trim %) #"###")
                           (filter
                            #(not (empty? (string/trim %)))
                            (line-seq rf)))))]
    (fn [prop_separators propnum_separators props]
      (let* [prop_separators
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
                       prop_source)))

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
                     (map search-result prop_lst)))))))

(defn test-ssh-exec-cmds [host port user password commands proxyhost proxyport]
  (Thread/sleep (* (rand-int 5) 1000))
  (str "i am " host "=====\n"))

(defn get-one-server-info [host]
  (test-ssh-exec-cmds host 63572 "youease" "3841c3847a98da37da83a212a8d4c14e"
                      ["sudo su - sislcb"
                       "cat /home/sislcb/client/ini/config.xml | grep server | grep -v id"
                       "cat /home/sislcb/gm_server/conf/keyconf.ini"]
                      "125.90.93.53" 36000))


(defn get-gm-new-servers [gametype startid endid]
  (let [results (atom {})]))

(defn get-gm-new-servers [gametype startid endid]
  (let [get-pro (fn [sid]
                  (let [ret (promise)]
                    (future (deliver
                             ret (get-one-server-info
                                  (format "%s%d.198game.com" gametype sid))))
                    ret))]
    (string/join "\n"
                 (map #(deref %)
                      (map #(get-pro %) (range startid (+ endid 1)))))))


(defn count-sub [s sub]
  (let [index (.indexOf s sub)]
    (if (= index -1)
      0
      (+ (count-sub (.substring s (+ index 1)) sub) 1))))

;; (print (count-sub "abcdefgabclsfd" "abc"))
;; (print (count-sub "sllabcabcdefgabclsfd" "abc"))
;; (print (count-sub "aaaaa" "aa"))
;; (print (count-sub "sldfl" "aa"))



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


;; (let [ret (atom [])]
;;   (future (swap! ret conj (get-one-server-info
;;                            "s8.youease.net")))
  
;;   (print @ret))

