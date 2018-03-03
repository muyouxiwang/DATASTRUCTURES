(ns jvtools.core-test
  (:require [clojure.test :refer :all]
            [jvtools.core :refer :all]
            [clojure.string :as string]))




#_(deftest ssh-exec-cmds-test
    (testing "test ssh commands"
      
      (is (> (let [ret (ssh-exec-cmds "192.168.1.64" 3333 
                                      "muyouxiwang" "123456" 
                                      ["ls" "df -h" "who am i"])]
               (println ret)
               (count ret))  0))
      ))



#_(deftest issubstr-test
  (testing "test is substr"
    (is (true? (issubstr "abcdefg" "def")))
    (is (false? (issubstr "abcdefg" "kkk")))
    (is (true? (issubstr "ooppj" "oo")))
    )
  ) 


#_(deftest countsub-test
  (testing "test count substr"
    (is (= 1 (countsub "abcdefg" "def")))
    (is (= 2 (countsub "defcdefg" "def")))
    (is (= 0 (countsub "llooppqq" "def")))
    (is (= 3 (countsub "ppppp" "ppp")))
    (is (= 1 (countsub "kkk" "kkk")))
    ))


#_(deftest httpget-test
  (testing "test http get"
    (is (> (let [ret (jv-http-get "http://www.baidu.com")]
             (println ret)
             (count ret)) 0))
    (is (> (let [ret (org-http-get "http://www.baidu.com")]
             (println ret)
             (count ret)) 0))
    (is (> (let [ret (clj-http-get "http://www.baxxxxxxxu.com")]
             (println ret)
             (count ret)) 0))
    ))






#_(deftest read-file-seq-test
  (testing "test read file seq"
    (is (> (let [content
                 ;; (string/join "" (read-file-seq "./test/jvtools/core_test.clj"))]
                 (read-file-seq "./test/jvtools/core_test.clj"
                                (fn [content] (string/join "\n" content)))]
             (println content)
             (count content)) 0))
    ))

#_(deftest str2pattern-test
  (testing "test str2pattern"
    (is (= (re-find (str2pattern "a.") "clsdkfakoopsdf") "ak"))
    (is (= (re-find (str2pattern "\\s") "clsdkfako\topsdf") "\t"))
    ))

#_(deftest clear-sp-test
  (testing "test clear sp"
    (is (= (clear-sp "asd\tsldf  sdll") "asdsldfsdll"))
    (is (= (clear-sp " oopp q\n") "ooppq"))
    ))

#_(deftest str-split-test
  (testing "test str split"
    (is (= (str-split "abcdefckjp" "c") ["ab" "def" "kjp"]))
    (is (= (str-split "oo,p,kk," ",") ["oo" "p" "kk" ""]))
    (is (= (str-split "ooahkoopqdoo" "oo") ["" "ahk" "pqd" ""]))
    (is (= (str-split "cfghmdppp" "hmd") ["cfg" "ppp"]))
    (is (= (str-split "ii*hjkl*pp" "*") ["ii" "hjkl" "pp"]))
    (is (= (str-split "武将灵珠×100" "×") ["武将灵珠" "100"]))
    ))
