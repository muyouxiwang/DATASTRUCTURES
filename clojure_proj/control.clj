(ns control
  (:import (java.util.regex Pattern)
           (java.util Properties)
           (com.jcraft.jsch JSch Session ProxyHTTP)

           (java.net URL URLConnection)
           (org.apache.http.impl.client DefaultHttpClient)
           (org.apache.http HttpEntity HttpResponse HttpRequest)
           (org.apache.http.client.methods HttpGet)
           (org.apache.http.util EntityUtils)
           )
  (:require [clojure.string :as string]
            [clojure.java.io :as io] 
            ))

(defn ssh-exec-cmds
  ([host port user password commands]
   (ssh-exec-cmds host port user password commands nil nil))

  ([host port user password commands proxyhost proxyport]
   (let* [jsch (JSch.)
          jsch-config (doto (Properties.)
                        (.put "StrictHostKeyChecking" "no"))
          proxy (if (and proxyhost proxyport)
                  (ProxyHTTP. proxyhost proxyport))
          session (doto (let [-session (.getSession jsch user host port)]
                          (doto -session
                            (.setConfig jsch-config)
                            (.setPassword password)
                            #_(.setTimeout 600))
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
         
         (let [shell-println (fn [cmd]
                               (.write out (str (string/trim cmd) "\n"))
                               ;; (.write out (.getBytes (str (string/trim cmd) "\n")))
                               (.flush out))

               shell-read-all (fn []
                                (while (or (.ready in) (Thread/sleep 1000) (.ready in))
                                  ;; (while (or (> (.available in) 0) (Thread/sleep 1000) (> (.available in) 0))
                                  (.append buff (char (.read in)))))]
           
           (shell-read-all)
           (doseq [cmd commands]
             (shell-println cmd)
             (shell-read-all)))
         (.toString buff))
       (catch Exception e (str "[get server info error] " e))
       (finally (.disconnect channel)
                (.disconnect session))))))

;; (let [ret (atom [])
;;       o1 (Thread. #(swap! ret conj (str "11111111111" (ssh-exec-cmds
;;                                                        "192.168.0.109" 3333 "muyouxiwang" "123456" 
;;                                                        [
;;                                                         "who am i"
;;                                                         "who am i"]) "111111111111")))
;;       o2 (Thread. #(swap! ret conj (str "2222222222222" (ssh-exec-cmds
;;                                                        "192.168.0.109" 3333 "root" "123456" 
;;                                                        [
;;                                                         "who am i"
;;                                                         "who am i"]) "22222222222222222")))
;;       ]
;;   (.start o1)
;;   (.start o2)
;;   (.join o1)
;;   (.join o2)
;;   (print @ret)
;;   )



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


(defn make_props [prop_separators propnum_separators props]
  (let* [prop_source
         (future (with-open [rf (io/reader "./sourcefile.xml")]
                   (reduce conj [] (map
                                    #(string/split (string/trim %) #"###")
                                    (filter
                                     #(not (empty? (string/trim %)))
                                     (line-seq rf))))))
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
                      prop_seq)))
         one-item-results (fn [search_name num]
                            (filter #(not (nil? %))
                                    (map #(let [[pname prop_str] %]
                                            (if (not (= (.indexOf pname search_name) -1))
                                              (if (not (= (.indexOf prop_str "%d") -1))
                                                (format prop_str num)
                                                prop_str)))
                                         @prop_source)))
         search-result (fn [item]
                         (reduce into []
                                 (map #(if (not (= (.indexOf item %) -1))
                                         (let [[search_name num]
                                               (string/split item
                                                             (Pattern/compile %))]
                                           (one-item-results
                                            search_name (Integer/parseInt num))))
                                      propnum_separators)))]

    (reduce into [] 
            (map #(if (= (count %) 0) ["??????????????"] %)
                 (map search-result prop_lst)))))

;; (doseq [line (make_props
;;               "，|、|,"
;;               "*|×|x"
;;               "宝石25×15，紅鑽石30×2，藍鑽石30×8，黃鑽石30×6，未知30×4，未知30+6")]
;;   (println line)
;;   )


#_(defn test-ssh-exec-cmds [host port user password commands proxyhost proxyport]
    (Thread/sleep (* (rand-int 5) 1000))
    (str "i am " host "=====\n"))



(defn get-gm-new-servers [gametype startid endid]
  (if (and (> startid 0)
           (> endid 0)
           (>= endid startid))
    (let [get-pro (fn [sid]
                    (future (ssh-exec-cmds (format "%s%d.198game.com" gametype sid)
                                           63572 "youease" "3841c3847a98da37da83a212a8d4c14e"
                                           ["sudo su - sislcb"
                                            "cat /home/sislcb/client/ini/config.xml | grep server | grep -v id"
                                            "cat /home/sislcb/gm_server/conf/keyconf.ini"]
                                           "125.90.93.53" 36000)))]
      (string/join "\n******************************************\n"
                   (map #(deref %)
                        (map #(get-pro %) (range startid (+ endid 1))))))))


(defn count-sub [s sub]
  (let [index (.indexOf s sub)]
    (if (= index -1)
      0
      (+ (count-sub (.substring s (+ index 1)) sub) 1))))

;; (print (count-sub "abcdefgabclsfd" "abc"))
;; (print (count-sub "sllabcabcdefgabclsfd" "abc"))
;; (print (count-sub "aaaaa" "aa"))
;; (print (count-sub "sldfl" "aa"))




;; (print (issubstr "abcdefg" "def"))
;; (print (issubstr "abcdefg" "uil"))

;; (with-open [rf (io/reader "大部分运营商（幻三）  1月26日（充值送好礼）.xml")]
;;   (let [content (string/join "\n" (hs2ms2qq (line-seq rf) "hs2ms"))]
;;     (spit "result_ms.xml" content)))
;; (with-open [rf (io/reader "大部分运营商（幻三）  1月26日（充值送好礼）.xml")]
;;   (let [content (string/join "\n" (hs2ms2qq (line-seq rf) "hs2qq"))]
;;     (spit "result_qq.xml" content)))

(defn http-get [url]
  (try
    (let* [con (doto (.openConnection (URL. url))
                 (.setRequestProperty "accept" "*/*")
                 (.setRequestProperty "connection" "Keep-Alive")
                 (.setRequestProperty
                  "user-agent"
                  "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1;SV1)")
                 (.connect))
           ret (StringBuilder.)]
      (with-open [in (io/reader (.getInputStream con))]
        (while (or (.ready in) (Thread/sleep 1000) (.ready in))
          (.append ret (char (.read in)))))
      (.toString ret))
    (catch Exception e
      (str "[net error] " e))))
      
(defn org-http-get [url]
  (let* [client (DefaultHttpClient.)
         request (HttpGet. url)]
    (try
      (EntityUtils/toString (.getEntity (.execute client request)))
      (catch Exception e
        (str "[net error] " e)))))




        
;; (print (org-http-get "http://www.baidu.com"))
;; (print (http-get "http://www.baidu.com"))


;; java -cp ./;clojure-1.8.0.jar;jsch-0.1.54.jar;httpcore-4.4.9.jar;httpclient-4.5.5.jar;commons-logging-1.2.jar clojure.main control.clj



