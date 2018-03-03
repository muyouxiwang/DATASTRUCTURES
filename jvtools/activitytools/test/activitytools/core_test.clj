(ns activitytools.core-test
  (:require [clojure.test :refer :all]
            ;; [activitytools.gui :refer :all]
            [activitytools.control :refer :all]
            [clojure.string]))

#_(deftest a-test
  (testing "FIXME, I fail."
    (is (= 0 1))))



(deftest polish-gm-result-test
  (testing "test polish result"
    (is (> (count
            (let* [content
                   (str
                    "Last login: Sat Mar  3 09:44:38 2018 from 125.90.93.53\n"
                    "[youease@s953shizhi ~]$ sudo su - sislcb\n"
                    "[sislcb@s953shizhi ~]$ grep \"<server_name>\" /home/sislcb/client/ini/config.xml |  awk -F \">\" '{print $2}' | awk -F \"<\" '{print $1}'\n"
                    "s953 ¹Ï¹ûÆ®Ïã\n"
                    "[sislcb@s953shizhi ~]$ cat /home/sislcb/key.log | grep -v sepwd\n"
                    "uid = VL1IX4xUC1uGgcLfDHG3DAH0K\n"
                    "\n"
                    "cliend = NFvZAlFcNhA2gM6rMBmpjz810sgnQvrDaWCLiMrzx3AiiaK6LBu6\n"
                    "\n"
                    "\n"
                    "key = s7nSN0YoYxZZSTgTzFZWK9yUIPO6VCJmcAgZJJmHKRGCeXwN7ZeQCNKkC4U308qnHblrod906jgNgg6nJjHlAWadt6JDHaZoPlPdzsn9L7pwmvnBj5WTuBBYblBSZAgPqAwt4TBiu2Pl1bWjKmHeZjHa9i39mNrhmYLVnndRR3dSIDGs2mb2aSFjFIW4voPmmAiJrwBj4iFMWPerHUtSNCGtlC2kvQISru7SvbFytPOUExlnriIfVocKvd61yhm1gunLFwODlD2ZERQ7ayPAr3PX\n"
                    "[sislcb@s953shizhi ~]$\n")
                   content (parse-gm-result "s953.198game.com" content)]
              (println content)
              content)) 0))
    ))
