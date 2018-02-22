
(ns tools
  (:import (javax.swing JFrame
                        JLabel
                        JTextField
                        JButton
                        JPanel
                        JTabbedPane)
           (java.awt GridLayout BorderLayout)
           (java.awt.event KeyEvent)
           #_(javax.swing.event *)
           (java.util.regex Pattern))
  (:require [clojure.string :as str]
            [clojure.java.io :as io]
            ))




(defn prop_source [filename]
  (with-open [rf (io/reader filename)]
    (reduce conj [] (map
                     #(str/split (str/trim %) #"###")
                     (filter
                      #(not (empty? (str/trim %)))
                      (line-seq rf))))))
(defn  make_props
  [prop_separators propnum_separators props]
  (let* [search_result  []
         prop_separators
         (str/split prop_separators #"|")
         propnum_separators
         (str/split propnum_separators #"|")
         prop_seq (first (filter
                          #(> (.indexOf props %) -1)
                          prop_separators))
         prop_lst (if (nil? prop_seq)
                    [props]
                    (str/split
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
                            (str/split item
                                       (Pattern/compile %))]
                        (one-item-results
                         search_name (Integer/parseInt num))))
                   propnum_separators)))

    (reduce into [] 
            (map #(if (= (count %) 0) "????----" %)
                 (map search-result prop_lst)))))
;; for item in prop_lst:
;;     exist = False
;;     for propnum_sep in propnum_separators:
;;         if propnum_sep in item:
;;             exist = True
;;             search_name, num = item.split(propnum_sep)
;;             search_name = search_name.strip()
;;             num = int(num.strip())
;;     if not exist:
;;         search_result.append("?" * 30)
;;         continue
;;     exist = False
;;     for pname, prop_str in prop_source:
;;         if search_name in pname:
;;             exist = True
;;             if prop_str.find('%d') != -1:
;;                 search_result.append(prop_str % num)
;;             else:
;;                 search_result.append(prop_str)
;;     if not exist:
;;         search_result.append("?" * 30)

;; return search_result






(defn main []

  ;; (print (prop_source "./sourcefile.xml"))
  (print (make_props "，|、|," "*|×|x"
    "宝石25×15，紅鑽石30×2，藍鑽石30×8，黃鑽石30×6，未知30×4，未知30+6"
                       ))
  )







(defn gui []
  (let [frame (JFrame. "tools")
        tabs (JTabbedPane. JTabbedPane/TOP)
        panel1 (JPanel.)
        panel2 (JPanel.)]
    (doto tabs
      (.add panel1 "道具查询")
      ;; (.setMnemonicAt 0 KeyEvent/VK_0)
      (.add panel2 "second")
      ;; (.setMnemonicAt 1 KeyEvent/VK_1)
      )
    (doto frame
      (.setDefaultCloseOperation
       (JFrame/EXIT_ON_CLOSE))
      (.setSize 300 200)
      (.setLayout (BorderLayout.))
      (.add tabs BorderLayout/CENTER)
      (.setVisible true))))


(gui)
;; (main)

;; java -cp clojure-1.8.0.jar clojure.main tools.clj
