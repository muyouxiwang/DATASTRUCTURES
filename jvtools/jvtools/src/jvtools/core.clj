(ns jvtools.core
  (:import
   (java.util.regex Pattern)
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
            [clj-http.client :as client]
            )
  )


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

(defn issubstr [s su]
  (not (= (.indexOf s su) -1)))  


(defn countsub [s sub]
  (let [index (.indexOf s sub)]
    (if (= index -1)
      0
      (+ (countsub (subs s (+ index 1)) sub) 1))))


(defn jv-http-get [url]
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


(defn clj-http-get [url]
  (try
    (client/get url)
    (catch Exception e
      (str "[net error] " e))))


(defn read-file-seq [filename fn]
  (with-open [rf (io/reader filename)]
    (doall (fn (line-seq rf)))))


(defn str2pattern [s]
  (Pattern/compile s))


(defn clear-sp [s]
  (string/replace s #"\s" ""))


(defn str-split [s sub]
  (let [i (string/index-of s sub)
        l (count sub)]
    (if i
      (into [(subs s 0 i)]
            (str-split (subs s (+ i l)) sub))
      [s])))
