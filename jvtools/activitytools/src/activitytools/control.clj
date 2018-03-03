(ns activitytools.control

  (:require [clojure.string :as string]
            [jvtools.core :refer :all]
            ))


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
              (issubstr % minmoney) (let [index (string/index-of % minmoney_end)]
                                      (str (subs % 0 index) "0" (subs % index)))
              (issubstr % award) (let [index (string/index-of % award_end)]
                                   (str (subs % 0 index) "0" (subs % index)))
              :else %) h3xml)
      (= trans_type "hs2qq")
      (map #(cond
              (issubstr % moneytype) (string/replace % moneytype new_moneytype)
              (issubstr % minmoney) (let [index (string/index-of % minmoney_end)]
                                      (str (subs % 0 index) "00" (subs % index)))
              (issubstr % award) (let [index (string/index-of % award_end)]
                                   (str (subs % 0 index) "00" (subs % index)))
              :else %) h3xml))))


(defn make_props [prop_separators propnum_separators props]
  (let* [prop_source
         (future 
           (reduce conj [] (read-file-seq
                            "./sourcefile.xml"
                            (fn [lines]
                              (map
                               #(string/split (string/trim %) #"###")
                               (filter
                                #(not (empty? (string/trim %)))
                                lines))))))
         prop_separators
         (string/split prop_separators #"\|")
         propnum_separators
         (string/split propnum_separators #"\|")
         prop_seq (first (filter
                          #(string/index-of props %)
                          prop_separators))
         prop_lst (if (nil? prop_seq)
                    [props]
                    (str-split props prop_seq))
         one-item-results (fn [search_name num]
                            (filter #(not (nil? %))
                                    (map
                                     #(let [[pname prop_str] %]
                                        (if (string/index-of pname search_name)
                                          (if (string/index-of prop_str "%d")
                                            (format prop_str num)
                                            prop_str)))
                                     @prop_source)))
         search-result (fn [item]
                         (reduce into
                                 []
                                 (let [item (clear-sp item)]
                                   (map #(if (string/index-of item %)
                                           (let [[search_name num]
                                                 (str-split item %)]
                                             (one-item-results
                                              search_name (Integer/parseInt num))))
                                        propnum_separators))))]
    (reduce into [] 
            (map #(if (= (count %) 0) ["??????????????"] %)
                 (map search-result prop_lst)))))


(defn parse-gm-result [url content]
  (apply
   str
   url
   "\n" (string/join
         "\n"
         (filter 
          #(not (or (empty? %) (re-find #"login|@|\$" %)))
          (map clear-sp (string/split content #"\n"))))))


(defn get-gm-new-servers [gametype startid endid]
  (if (and (> startid 0)
           (> endid 0)
           (>= endid startid))
    (let [get-pro (fn [sid]
                    (let* [url (format "%s%d.198game.com" gametype sid)]
                      (future
                        (parse-gm-result
                         url
                         (ssh-exec-cmds
                          url
                          63572 "youease" "3841c3847a98da37da83a212a8d4c14e"
                          ["sudo su - sislcb"
                           "grep \"<server_name>\" /home/sislcb/client/ini/config.xml | awk -F \">\" '{print $2}' | awk -F \"<\" '{print $1}' "
                           "cat /home/sislcb/key.log | grep -v sepwd"]
                          "125.90.93.53" 36000)))))]
      (string/join (str "\n" (apply str (repeat 50 \*)) "\n")
                   (map #(deref %)
                        (map #(get-pro %) (range startid (+ endid 1))))))))




