#!/usr/bin/env python
# coding: utf-8

# # Corona Genome Analysis

# #### Let's start by retreiving the complete genome of Coronavirus. The records are extracted from the wuhan region. Source: https://www.ncbi.nlm.nih.gov/nuccore/NC_045512
# 
# >Orthocoronavirinae, in the family Coronaviridae, order Nidovirales, and realm Riboviria. They are enveloped viruses with a positive-sense single-stranded RNA genome and a nucleocapsid of helical symmetry. This is wrapped in a icosahedral protein shell. The genome size of coronaviruses ranges from approximately 26 to 32 kilobases, one of the largest among RNA viruses. They have characteristic club-shaped spikes that project from their surface, which in electron micrographs create an image reminiscent of the solar corona, from which their name derives.
# 
# <img src="https://raw.githubusercontent.com/Bhard27/COVID-Genome-DS/master/images_copy/wiki.png" width="480">
# 
# > **Basic Information:** Coronavirus is a single stranded RNA-virus (DNA is double stranded). RNA polymers are made up of nucleotides. These nucleotides have three parts: 1) a five carbon Ribose sugar, 2) a phosphate molecule and 3) one of four nitrogenous bases: adenine(a), guanine(g), cytosine(c) or uracil(u) / thymine(t). 
# 
# > Thymine is found in DNA and Uracil in RNA. But for following analysis, you can consider (u) and (t) to be analogous. 
# 
# 
# <img src="https://raw.githubusercontent.com/Bhard27/COVID-Genome-DS/master/images_copy/parts-of-nucleotide.jpg" width="480">

# In[ ]:


corona = """
        1 attaaaggtt tataccttcc caggtaacaa accaaccaac tttcgatctc ttgtagatct
       61 gttctctaaa cgaactttaa aatctgtgtg gctgtcactc ggctgcatgc ttagtgcact
      121 cacgcagtat aattaataac taattactgt cgttgacagg acacgagtaa ctcgtctatc
      181 ttctgcaggc tgcttacggt ttcgtccgtg ttgcagccga tcatcagcac atctaggttt
      241 cgtccgggtg tgaccgaaag gtaagatgga gagccttgtc cctggtttca acgagaaaac
      301 acacgtccaa ctcagtttgc ctgttttaca ggttcgcgac gtgctcgtac gtggctttgg
      361 agactccgtg gaggaggtct tatcagaggc acgtcaacat cttaaagatg gcacttgtgg
      421 cttagtagaa gttgaaaaag gcgttttgcc tcaacttgaa cagccctatg tgttcatcaa
      481 acgttcggat gctcgaactg cacctcatgg tcatgttatg gttgagctgg tagcagaact
      541 cgaaggcatt cagtacggtc gtagtggtga gacacttggt gtccttgtcc ctcatgtggg
      601 cgaaatacca gtggcttacc gcaaggttct tcttcgtaag aacggtaata aaggagctgg
      661 tggccatagt tacggcgccg atctaaagtc atttgactta ggcgacgagc ttggcactga
      721 tccttatgaa gattttcaag aaaactggaa cactaaacat agcagtggtg ttacccgtga
      781 actcatgcgt gagcttaacg gaggggcata cactcgctat gtcgataaca acttctgtgg
      841 ccctgatggc taccctcttg agtgcattaa agaccttcta gcacgtgctg gtaaagcttc
      901 atgcactttg tccgaacaac tggactttat tgacactaag aggggtgtat actgctgccg
      961 tgaacatgag catgaaattg cttggtacac ggaacgttct gaaaagagct atgaattgca
     1021 gacacctttt gaaattaaat tggcaaagaa atttgacacc ttcaatgggg aatgtccaaa
     1081 ttttgtattt cccttaaatt ccataatcaa gactattcaa ccaagggttg aaaagaaaaa
     1141 gcttgatggc tttatgggta gaattcgatc tgtctatcca gttgcgtcac caaatgaatg
     1201 caaccaaatg tgcctttcaa ctctcatgaa gtgtgatcat tgtggtgaaa cttcatggca
     1261 gacgggcgat tttgttaaag ccacttgcga attttgtggc actgagaatt tgactaaaga
     1321 aggtgccact acttgtggtt acttacccca aaatgctgtt gttaaaattt attgtccagc
     1381 atgtcacaat tcagaagtag gacctgagca tagtcttgcc gaataccata atgaatctgg
     1441 cttgaaaacc attcttcgta agggtggtcg cactattgcc tttggaggct gtgtgttctc
     1501 ttatgttggt tgccataaca agtgtgccta ttgggttcca cgtgctagcg ctaacatagg
     1561 ttgtaaccat acaggtgttg ttggagaagg ttccgaaggt cttaatgaca accttcttga
     1621 aatactccaa aaagagaaag tcaacatcaa tattgttggt gactttaaac ttaatgaaga
     1681 gatcgccatt attttggcat ctttttctgc ttccacaagt gcttttgtgg aaactgtgaa
     1741 aggtttggat tataaagcat tcaaacaaat tgttgaatcc tgtggtaatt ttaaagttac
     1801 aaaaggaaaa gctaaaaaag gtgcctggaa tattggtgaa cagaaatcaa tactgagtcc
     1861 tctttatgca tttgcatcag aggctgctcg tgttgtacga tcaattttct cccgcactct
     1921 tgaaactgct caaaattctg tgcgtgtttt acagaaggcc gctataacaa tactagatgg
     1981 aatttcacag tattcactga gactcattga tgctatgatg ttcacatctg atttggctac
     2041 taacaatcta gttgtaatgg cctacattac aggtggtgtt gttcagttga cttcgcagtg
     2101 gctaactaac atctttggca ctgtttatga aaaactcaaa cccgtccttg attggcttga
     2161 agagaagttt aaggaaggtg tagagtttct tagagacggt tgggaaattg ttaaatttat
     2221 ctcaacctgt gcttgtgaaa ttgtcggtgg acaaattgtc acctgtgcaa aggaaattaa
     2281 ggagagtgtt cagacattct ttaagcttgt aaataaattt ttggctttgt gtgctgactc
     2341 tatcattatt ggtggagcta aacttaaagc cttgaattta ggtgaaacat ttgtcacgca
     2401 ctcaaaggga ttgtacagaa agtgtgttaa atccagagaa gaaactggcc tactcatgcc
     2461 tctaaaagcc ccaaaagaaa ttatcttctt agagggagaa acacttccca cagaagtgtt
     2521 aacagaggaa gttgtcttga aaactggtga tttacaacca ttagaacaac ctactagtga
     2581 agctgttgaa gctccattgg ttggtacacc agtttgtatt aacgggctta tgttgctcga
     2641 aatcaaagac acagaaaagt actgtgccct tgcacctaat atgatggtaa caaacaatac
     2701 cttcacactc aaaggcggtg caccaacaaa ggttactttt ggtgatgaca ctgtgataga
     2761 agtgcaaggt tacaagagtg tgaatatcac ttttgaactt gatgaaagga ttgataaagt
     2821 acttaatgag aagtgctctg cctatacagt tgaactcggt acagaagtaa atgagttcgc
     2881 ctgtgttgtg gcagatgctg tcataaaaac tttgcaacca gtatctgaat tacttacacc
     2941 actgggcatt gatttagatg agtggagtat ggctacatac tacttatttg atgagtctgg
     3001 tgagtttaaa ttggcttcac atatgtattg ttctttctac cctccagatg aggatgaaga
     3061 agaaggtgat tgtgaagaag aagagtttga gccatcaact caatatgagt atggtactga
     3121 agatgattac caaggtaaac ctttggaatt tggtgccact tctgctgctc ttcaacctga
     3181 agaagagcaa gaagaagatt ggttagatga tgatagtcaa caaactgttg gtcaacaaga
     3241 cggcagtgag gacaatcaga caactactat tcaaacaatt gttgaggttc aacctcaatt
     3301 agagatggaa cttacaccag ttgttcagac tattgaagtg aatagtttta gtggttattt
     3361 aaaacttact gacaatgtat acattaaaaa tgcagacatt gtggaagaag ctaaaaaggt
     3421 aaaaccaaca gtggttgtta atgcagccaa tgtttacctt aaacatggag gaggtgttgc
     3481 aggagcctta aataaggcta ctaacaatgc catgcaagtt gaatctgatg attacatagc
     3541 tactaatgga ccacttaaag tgggtggtag ttgtgtttta agcggacaca atcttgctaa
     3601 acactgtctt catgttgtcg gcccaaatgt taacaaaggt gaagacattc aacttcttaa
     3661 gagtgcttat gaaaatttta atcagcacga agttctactt gcaccattat tatcagctgg
     3721 tatttttggt gctgacccta tacattcttt aagagtttgt gtagatactg ttcgcacaaa
     3781 tgtctactta gctgtctttg ataaaaatct ctatgacaaa cttgtttcaa gctttttgga
     3841 aatgaagagt gaaaagcaag ttgaacaaaa gatcgctgag attcctaaag aggaagttaa
     3901 gccatttata actgaaagta aaccttcagt tgaacagaga aaacaagatg ataagaaaat
     3961 caaagcttgt gttgaagaag ttacaacaac tctggaagaa actaagttcc tcacagaaaa
     4021 cttgttactt tatattgaca ttaatggcaa tcttcatcca gattctgcca ctcttgttag
     4081 tgacattgac atcactttct taaagaaaga tgctccatat atagtgggtg atgttgttca
     4141 agagggtgtt ttaactgctg tggttatacc tactaaaaag gctggtggca ctactgaaat
     4201 gctagcgaaa gctttgagaa aagtgccaac agacaattat ataaccactt acccgggtca
     4261 gggtttaaat ggttacactg tagaggaggc aaagacagtg cttaaaaagt gtaaaagtgc
     4321 cttttacatt ctaccatcta ttatctctaa tgagaagcaa gaaattcttg gaactgtttc
     4381 ttggaatttg cgagaaatgc ttgcacatgc agaagaaaca cgcaaattaa tgcctgtctg
     4441 tgtggaaact aaagccatag tttcaactat acagcgtaaa tataagggta ttaaaataca
     4501 agagggtgtg gttgattatg gtgctagatt ttacttttac accagtaaaa caactgtagc
     4561 gtcacttatc aacacactta acgatctaaa tgaaactctt gttacaatgc cacttggcta
     4621 tgtaacacat ggcttaaatt tggaagaagc tgctcggtat atgagatctc tcaaagtgcc
     4681 agctacagtt tctgtttctt cacctgatgc tgttacagcg tataatggtt atcttacttc
     4741 ttcttctaaa acacctgaag aacattttat tgaaaccatc tcacttgctg gttcctataa
     4801 agattggtcc tattctggac aatctacaca actaggtata gaatttctta agagaggtga
     4861 taaaagtgta tattacacta gtaatcctac cacattccac ctagatggtg aagttatcac
     4921 ctttgacaat cttaagacac ttctttcttt gagagaagtg aggactatta aggtgtttac
     4981 aacagtagac aacattaacc tccacacgca agttgtggac atgtcaatga catatggaca
     5041 acagtttggt ccaacttatt tggatggagc tgatgttact aaaataaaac ctcataattc
     5101 acatgaaggt aaaacatttt atgttttacc taatgatgac actctacgtg ttgaggcttt
     5161 tgagtactac cacacaactg atcctagttt tctgggtagg tacatgtcag cattaaatca
     5221 cactaaaaag tggaaatacc cacaagttaa tggtttaact tctattaaat gggcagataa
     5281 caactgttat cttgccactg cattgttaac actccaacaa atagagttga agtttaatcc
     5341 acctgctcta caagatgctt attacagagc aagggctggt gaagctgcta acttttgtgc
     5401 acttatctta gcctactgta ataagacagt aggtgagtta ggtgatgtta gagaaacaat
     5461 gagttacttg tttcaacatg ccaatttaga ttcttgcaaa agagtcttga acgtggtgtg
     5521 taaaacttgt ggacaacagc agacaaccct taagggtgta gaagctgtta tgtacatggg
     5581 cacactttct tatgaacaat ttaagaaagg tgttcagata ccttgtacgt gtggtaaaca
     5641 agctacaaaa tatctagtac aacaggagtc accttttgtt atgatgtcag caccacctgc
     5701 tcagtatgaa cttaagcatg gtacatttac ttgtgctagt gagtacactg gtaattacca
     5761 gtgtggtcac tataaacata taacttctaa agaaactttg tattgcatag acggtgcttt
     5821 acttacaaag tcctcagaat acaaaggtcc tattacggat gttttctaca aagaaaacag
     5881 ttacacaaca accataaaac cagttactta taaattggat ggtgttgttt gtacagaaat
     5941 tgaccctaag ttggacaatt attataagaa agacaattct tatttcacag agcaaccaat
     6001 tgatcttgta ccaaaccaac catatccaaa cgcaagcttc gataatttta agtttgtatg
     6061 tgataatatc aaatttgctg atgatttaaa ccagttaact ggttataaga aacctgcttc
     6121 aagagagctt aaagttacat ttttccctga cttaaatggt gatgtggtgg ctattgatta
     6181 taaacactac acaccctctt ttaagaaagg agctaaattg ttacataaac ctattgtttg
     6241 gcatgttaac aatgcaacta ataaagccac gtataaacca aatacctggt gtatacgttg
     6301 tctttggagc acaaaaccag ttgaaacatc aaattcgttt gatgtactga agtcagagga
     6361 cgcgcaggga atggataatc ttgcctgcga agatctaaaa ccagtctctg aagaagtagt
     6421 ggaaaatcct accatacaga aagacgttct tgagtgtaat gtgaaaacta ccgaagttgt
     6481 aggagacatt atacttaaac cagcaaataa tagtttaaaa attacagaag aggttggcca
     6541 cacagatcta atggctgctt atgtagacaa ttctagtctt actattaaga aacctaatga
     6601 attatctaga gtattaggtt tgaaaaccct tgctactcat ggtttagctg ctgttaatag
     6661 tgtcccttgg gatactatag ctaattatgc taagcctttt cttaacaaag ttgttagtac
     6721 aactactaac atagttacac ggtgtttaaa ccgtgtttgt actaattata tgccttattt
     6781 ctttacttta ttgctacaat tgtgtacttt tactagaagt acaaattcta gaattaaagc
     6841 atctatgccg actactatag caaagaatac tgttaagagt gtcggtaaat tttgtctaga
     6901 ggcttcattt aattatttga agtcacctaa tttttctaaa ctgataaata ttataatttg
     6961 gtttttacta ttaagtgttt gcctaggttc tttaatctac tcaaccgctg ctttaggtgt
     7021 tttaatgtct aatttaggca tgccttctta ctgtactggt tacagagaag gctatttgaa
     7081 ctctactaat gtcactattg caacctactg tactggttct ataccttgta gtgtttgtct
     7141 tagtggttta gattctttag acacctatcc ttctttagaa actatacaaa ttaccatttc
     7201 atcttttaaa tgggatttaa ctgcttttgg cttagttgca gagtggtttt tggcatatat
     7261 tcttttcact aggtttttct atgtacttgg attggctgca atcatgcaat tgtttttcag
     7321 ctattttgca gtacatttta ttagtaattc ttggcttatg tggttaataa ttaatcttgt
     7381 acaaatggcc ccgatttcag ctatggttag aatgtacatc ttctttgcat cattttatta
     7441 tgtatggaaa agttatgtgc atgttgtaga cggttgtaat tcatcaactt gtatgatgtg
     7501 ttacaaacgt aatagagcaa caagagtcga atgtacaact attgttaatg gtgttagaag
     7561 gtccttttat gtctatgcta atggaggtaa aggcttttgc aaactacaca attggaattg
     7621 tgttaattgt gatacattct gtgctggtag tacatttatt agtgatgaag ttgcgagaga
     7681 cttgtcacta cagtttaaaa gaccaataaa tcctactgac cagtcttctt acatcgttga
     7741 tagtgttaca gtgaagaatg gttccatcca tctttacttt gataaagctg gtcaaaagac
     7801 ttatgaaaga cattctctct ctcattttgt taacttagac aacctgagag ctaataacac
     7861 taaaggttca ttgcctatta atgttatagt ttttgatggt aaatcaaaat gtgaagaatc
     7921 atctgcaaaa tcagcgtctg tttactacag tcagcttatg tgtcaaccta tactgttact
     7981 agatcaggca ttagtgtctg atgttggtga tagtgcggaa gttgcagtta aaatgtttga
     8041 tgcttacgtt aatacgtttt catcaacttt taacgtacca atggaaaaac tcaaaacact
     8101 agttgcaact gcagaagctg aacttgcaaa gaatgtgtcc ttagacaatg tcttatctac
     8161 ttttatttca gcagctcggc aagggtttgt tgattcagat gtagaaacta aagatgttgt
     8221 tgaatgtctt aaattgtcac atcaatctga catagaagtt actggcgata gttgtaataa
     8281 ctatatgctc acctataaca aagttgaaaa catgacaccc cgtgaccttg gtgcttgtat
     8341 tgactgtagt gcgcgtcata ttaatgcgca ggtagcaaaa agtcacaaca ttgctttgat
     8401 atggaacgtt aaagatttca tgtcattgtc tgaacaacta cgaaaacaaa tacgtagtgc
     8461 tgctaaaaag aataacttac cttttaagtt gacatgtgca actactagac aagttgttaa
     8521 tgttgtaaca acaaagatag cacttaaggg tggtaaaatt gttaataatt ggttgaagca
     8581 gttaattaaa gttacacttg tgttcctttt tgttgctgct attttctatt taataacacc
     8641 tgttcatgtc atgtctaaac atactgactt ttcaagtgaa atcataggat acaaggctat
     8701 tgatggtggt gtcactcgtg acatagcatc tacagatact tgttttgcta acaaacatgc
     8761 tgattttgac acatggttta gccagcgtgg tggtagttat actaatgaca aagcttgccc
     8821 attgattgct gcagtcataa caagagaagt gggttttgtc gtgcctggtt tgcctggcac
     8881 gatattacgc acaactaatg gtgacttttt gcatttctta cctagagttt ttagtgcagt
     8941 tggtaacatc tgttacacac catcaaaact tatagagtac actgactttg caacatcagc
     9001 ttgtgttttg gctgctgaat gtacaatttt taaagatgct tctggtaagc cagtaccata
     9061 ttgttatgat accaatgtac tagaaggttc tgttgcttat gaaagtttac gccctgacac
     9121 acgttatgtg ctcatggatg gctctattat tcaatttcct aacacctacc ttgaaggttc
     9181 tgttagagtg gtaacaactt ttgattctga gtactgtagg cacggcactt gtgaaagatc
     9241 agaagctggt gtttgtgtat ctactagtgg tagatgggta cttaacaatg attattacag
     9301 atctttacca ggagttttct gtggtgtaga tgctgtaaat ttacttacta atatgtttac
     9361 accactaatt caacctattg gtgctttgga catatcagca tctatagtag ctggtggtat
     9421 tgtagctatc gtagtaacat gccttgccta ctattttatg aggtttagaa gagcttttgg
     9481 tgaatacagt catgtagttg cctttaatac tttactattc cttatgtcat tcactgtact
     9541 ctgtttaaca ccagtttact cattcttacc tggtgtttat tctgttattt acttgtactt
     9601 gacattttat cttactaatg atgtttcttt tttagcacat attcagtgga tggttatgtt
     9661 cacaccttta gtacctttct ggataacaat tgcttatatc atttgtattt ccacaaagca
     9721 tttctattgg ttctttagta attacctaaa gagacgtgta gtctttaatg gtgtttcctt
     9781 tagtactttt gaagaagctg cgctgtgcac ctttttgtta aataaagaaa tgtatctaaa
     9841 gttgcgtagt gatgtgctat tacctcttac gcaatataat agatacttag ctctttataa
     9901 taagtacaag tattttagtg gagcaatgga tacaactagc tacagagaag ctgcttgttg
     9961 tcatctcgca aaggctctca atgacttcag taactcaggt tctgatgttc tttaccaacc
    10021 accacaaacc tctatcacct cagctgtttt gcagagtggt tttagaaaaa tggcattccc
    10081 atctggtaaa gttgagggtt gtatggtaca agtaacttgt ggtacaacta cacttaacgg
    10141 tctttggctt gatgacgtag tttactgtcc aagacatgtg atctgcacct ctgaagacat
    10201 gcttaaccct aattatgaag atttactcat tcgtaagtct aatcataatt tcttggtaca
    10261 ggctggtaat gttcaactca gggttattgg acattctatg caaaattgtg tacttaagct
    10321 taaggttgat acagccaatc ctaagacacc taagtataag tttgttcgca ttcaaccagg
    10381 acagactttt tcagtgttag cttgttacaa tggttcacca tctggtgttt accaatgtgc
    10441 tatgaggccc aatttcacta ttaagggttc attccttaat ggttcatgtg gtagtgttgg
    10501 ttttaacata gattatgact gtgtctcttt ttgttacatg caccatatgg aattaccaac
    10561 tggagttcat gctggcacag acttagaagg taacttttat ggaccttttg ttgacaggca
    10621 aacagcacaa gcagctggta cggacacaac tattacagtt aatgttttag cttggttgta
    10681 cgctgctgtt ataaatggag acaggtggtt tctcaatcga tttaccacaa ctcttaatga
    10741 ctttaacctt gtggctatga agtacaatta tgaacctcta acacaagacc atgttgacat
    10801 actaggacct ctttctgctc aaactggaat tgccgtttta gatatgtgtg cttcattaaa
    10861 agaattactg caaaatggta tgaatggacg taccatattg ggtagtgctt tattagaaga
    10921 tgaatttaca ccttttgatg ttgttagaca atgctcaggt gttactttcc aaagtgcagt
    10981 gaaaagaaca atcaagggta cacaccactg gttgttactc acaattttga cttcactttt
    11041 agttttagtc cagagtactc aatggtcttt gttctttttt ttgtatgaaa atgccttttt
    11101 accttttgct atgggtatta ttgctatgtc tgcttttgca atgatgtttg tcaaacataa
    11161 gcatgcattt ctctgtttgt ttttgttacc ttctcttgcc actgtagctt attttaatat
    11221 ggtctatatg cctgctagtt gggtgatgcg tattatgaca tggttggata tggttgatac
    11281 tagtttgtct ggttttaagc taaaagactg tgttatgtat gcatcagctg tagtgttact
    11341 aatccttatg acagcaagaa ctgtgtatga tgatggtgct aggagagtgt ggacacttat
    11401 gaatgtcttg acactcgttt ataaagttta ttatggtaat gctttagatc aagccatttc
    11461 catgtgggct cttataatct ctgttacttc taactactca ggtgtagtta caactgtcat
    11521 gtttttggcc agaggtattg tttttatgtg tgttgagtat tgccctattt tcttcataac
    11581 tggtaataca cttcagtgta taatgctagt ttattgtttc ttaggctatt tttgtacttg
    11641 ttactttggc ctcttttgtt tactcaaccg ctactttaga ctgactcttg gtgtttatga
    11701 ttacttagtt tctacacagg agtttagata tatgaattca cagggactac tcccacccaa
    11761 gaatagcata gatgccttca aactcaacat taaattgttg ggtgttggtg gcaaaccttg
    11821 tatcaaagta gccactgtac agtctaaaat gtcagatgta aagtgcacat cagtagtctt
    11881 actctcagtt ttgcaacaac tcagagtaga atcatcatct aaattgtggg ctcaatgtgt
    11941 ccagttacac aatgacattc tcttagctaa agatactact gaagcctttg aaaaaatggt
    12001 ttcactactt tctgttttgc tttccatgca gggtgctgta gacataaaca agctttgtga
    12061 agaaatgctg gacaacaggg caaccttaca agctatagcc tcagagttta gttcccttcc
    12121 atcatatgca gcttttgcta ctgctcaaga agcttatgag caggctgttg ctaatggtga
    12181 ttctgaagtt gttcttaaaa agttgaagaa gtctttgaat gtggctaaat ctgaatttga
    12241 ccgtgatgca gccatgcaac gtaagttgga aaagatggct gatcaagcta tgacccaaat
    12301 gtataaacag gctagatctg aggacaagag ggcaaaagtt actagtgcta tgcagacaat
    12361 gcttttcact atgcttagaa agttggataa tgatgcactc aacaacatta tcaacaatgc
    12421 aagagatggt tgtgttccct tgaacataat acctcttaca acagcagcca aactaatggt
    12481 tgtcatacca gactataaca catataaaaa tacgtgtgat ggtacaacat ttacttatgc
    12541 atcagcattg tgggaaatcc aacaggttgt agatgcagat agtaaaattg ttcaacttag
    12601 tgaaattagt atggacaatt cacctaattt agcatggcct cttattgtaa cagctttaag
    12661 ggccaattct gctgtcaaat tacagaataa tgagcttagt cctgttgcac tacgacagat
    12721 gtcttgtgct gccggtacta cacaaactgc ttgcactgat gacaatgcgt tagcttacta
    12781 caacacaaca aagggaggta ggtttgtact tgcactgtta tccgatttac aggatttgaa
    12841 atgggctaga ttccctaaga gtgatggaac tggtactatc tatacagaac tggaaccacc
    12901 ttgtaggttt gttacagaca cacctaaagg tcctaaagtg aagtatttat actttattaa
    12961 aggattaaac aacctaaata gaggtatggt acttggtagt ttagctgcca cagtacgtct
    13021 acaagctggt aatgcaacag aagtgcctgc caattcaact gtattatctt tctgtgcttt
    13081 tgctgtagat gctgctaaag cttacaaaga ttatctagct agtgggggac aaccaatcac
    13141 taattgtgtt aagatgttgt gtacacacac tggtactggt caggcaataa cagttacacc
    13201 ggaagccaat atggatcaag aatcctttgg tggtgcatcg tgttgtctgt actgccgttg
    13261 ccacatagat catccaaatc ctaaaggatt ttgtgactta aaaggtaagt atgtacaaat
    13321 acctacaact tgtgctaatg accctgtggg ttttacactt aaaaacacag tctgtaccgt
    13381 ctgcggtatg tggaaaggtt atggctgtag ttgtgatcaa ctccgcgaac ccatgcttca
    13441 gtcagctgat gcacaatcgt ttttaaacgg gtttgcggtg taagtgcagc ccgtcttaca
    13501 ccgtgcggca caggcactag tactgatgtc gtatacaggg cttttgacat ctacaatgat
    13561 aaagtagctg gttttgctaa attcctaaaa actaattgtt gtcgcttcca agaaaaggac
    13621 gaagatgaca atttaattga ttcttacttt gtagttaaga gacacacttt ctctaactac
    13681 caacatgaag aaacaattta taatttactt aaggattgtc cagctgttgc taaacatgac
    13741 ttctttaagt ttagaataga cggtgacatg gtaccacata tatcacgtca acgtcttact
    13801 aaatacacaa tggcagacct cgtctatgct ttaaggcatt ttgatgaagg taattgtgac
    13861 acattaaaag aaatacttgt cacatacaat tgttgtgatg atgattattt caataaaaag
    13921 gactggtatg attttgtaga aaacccagat atattacgcg tatacgccaa cttaggtgaa
    13981 cgtgtacgcc aagctttgtt aaaaacagta caattctgtg atgccatgcg aaatgctggt
    14041 attgttggtg tactgacatt agataatcaa gatctcaatg gtaactggta tgatttcggt
    14101 gatttcatac aaaccacgcc aggtagtgga gttcctgttg tagattctta ttattcattg
    14161 ttaatgccta tattaacctt gaccagggct ttaactgcag agtcacatgt tgacactgac
    14221 ttaacaaagc cttacattaa gtgggatttg ttaaaatatg acttcacgga agagaggtta
    14281 aaactctttg accgttattt taaatattgg gatcagacat accacccaaa ttgtgttaac
    14341 tgtttggatg acagatgcat tctgcattgt gcaaacttta atgttttatt ctctacagtg
    14401 ttcccaccta caagttttgg accactagtg agaaaaatat ttgttgatgg tgttccattt
    14461 gtagtttcaa ctggatacca cttcagagag ctaggtgttg tacataatca ggatgtaaac
    14521 ttacatagct ctagacttag ttttaaggaa ttacttgtgt atgctgctga ccctgctatg
    14581 cacgctgctt ctggtaatct attactagat aaacgcacta cgtgcttttc agtagctgca
    14641 cttactaaca atgttgcttt tcaaactgtc aaacccggta attttaacaa agacttctat
    14701 gactttgctg tgtctaaggg tttctttaag gaaggaagtt ctgttgaatt aaaacacttc
    14761 ttctttgctc aggatggtaa tgctgctatc agcgattatg actactatcg ttataatcta
    14821 ccaacaatgt gtgatatcag acaactacta tttgtagttg aagttgttga taagtacttt
    14881 gattgttacg atggtggctg tattaatgct aaccaagtca tcgtcaacaa cctagacaaa
    14941 tcagctggtt ttccatttaa taaatggggt aaggctagac tttattatga ttcaatgagt
    15001 tatgaggatc aagatgcact tttcgcatat acaaaacgta atgtcatccc tactataact
    15061 caaatgaatc ttaagtatgc cattagtgca aagaatagag ctcgcaccgt agctggtgtc
    15121 tctatctgta gtactatgac caatagacag tttcatcaaa aattattgaa atcaatagcc
    15181 gccactagag gagctactgt agtaattgga acaagcaaat tctatggtgg ttggcacaac
    15241 atgttaaaaa ctgtttatag tgatgtagaa aaccctcacc ttatgggttg ggattatcct
    15301 aaatgtgata gagccatgcc taacatgctt agaattatgg cctcacttgt tcttgctcgc
    15361 aaacatacaa cgtgttgtag cttgtcacac cgtttctata gattagctaa tgagtgtgct
    15421 caagtattga gtgaaatggt catgtgtggc ggttcactat atgttaaacc aggtggaacc
    15481 tcatcaggag atgccacaac tgcttatgct aatagtgttt ttaacatttg tcaagctgtc
    15541 acggccaatg ttaatgcact tttatctact gatggtaaca aaattgccga taagtatgtc
    15601 cgcaatttac aacacagact ttatgagtgt ctctatagaa atagagatgt tgacacagac
    15661 tttgtgaatg agttttacgc atatttgcgt aaacatttct caatgatgat actctctgac
    15721 gatgctgttg tgtgtttcaa tagcacttat gcatctcaag gtctagtggc tagcataaag
    15781 aactttaagt cagttcttta ttatcaaaac aatgttttta tgtctgaagc aaaatgttgg
    15841 actgagactg accttactaa aggacctcat gaattttgct ctcaacatac aatgctagtt
    15901 aaacagggtg atgattatgt gtaccttcct tacccagatc catcaagaat cctaggggcc
    15961 ggctgttttg tagatgatat cgtaaaaaca gatggtacac ttatgattga acggttcgtg
    16021 tctttagcta tagatgctta cccacttact aaacatccta atcaggagta tgctgatgtc
    16081 tttcatttgt acttacaata cataagaaag ctacatgatg agttaacagg acacatgtta
    16141 gacatgtatt ctgttatgct tactaatgat aacacttcaa ggtattggga acctgagttt
    16201 tatgaggcta tgtacacacc gcatacagtc ttacaggctg ttggggcttg tgttctttgc
    16261 aattcacaga cttcattaag atgtggtgct tgcatacgta gaccattctt atgttgtaaa
    16321 tgctgttacg accatgtcat atcaacatca cataaattag tcttgtctgt taatccgtat
    16381 gtttgcaatg ctccaggttg tgatgtcaca gatgtgactc aactttactt aggaggtatg
    16441 agctattatt gtaaatcaca taaaccaccc attagttttc cattgtgtgc taatggacaa
    16501 gtttttggtt tatataaaaa tacatgtgtt ggtagcgata atgttactga ctttaatgca
    16561 attgcaacat gtgactggac aaatgctggt gattacattt tagctaacac ctgtactgaa
    16621 agactcaagc tttttgcagc agaaacgctc aaagctactg aggagacatt taaactgtct
    16681 tatggtattg ctactgtacg tgaagtgctg tctgacagag aattacatct ttcatgggaa
    16741 gttggtaaac ctagaccacc acttaaccga aattatgtct ttactggtta tcgtgtaact
    16801 aaaaacagta aagtacaaat aggagagtac acctttgaaa aaggtgacta tggtgatgct
    16861 gttgtttacc gaggtacaac aacttacaaa ttaaatgttg gtgattattt tgtgctgaca
    16921 tcacatacag taatgccatt aagtgcacct acactagtgc cacaagagca ctatgttaga
    16981 attactggct tatacccaac actcaatatc tcagatgagt tttctagcaa tgttgcaaat
    17041 tatcaaaagg ttggtatgca aaagtattct acactccagg gaccacctgg tactggtaag
    17101 agtcattttg ctattggcct agctctctac tacccttctg ctcgcatagt gtatacagct
    17161 tgctctcatg ccgctgttga tgcactatgt gagaaggcat taaaatattt gcctatagat
    17221 aaatgtagta gaattatacc tgcacgtgct cgtgtagagt gttttgataa attcaaagtg
    17281 aattcaacat tagaacagta tgtcttttgt actgtaaatg cattgcctga gacgacagca
    17341 gatatagttg tctttgatga aatttcaatg gccacaaatt atgatttgag tgttgtcaat
    17401 gccagattac gtgctaagca ctatgtgtac attggcgacc ctgctcaatt acctgcacca
    17461 cgcacattgc taactaaggg cacactagaa ccagaatatt tcaattcagt gtgtagactt
    17521 atgaaaacta taggtccaga catgttcctc ggaacttgtc ggcgttgtcc tgctgaaatt
    17581 gttgacactg tgagtgcttt ggtttatgat aataagctta aagcacataa agacaaatca
    17641 gctcaatgct ttaaaatgtt ttataagggt gttatcacgc atgatgtttc atctgcaatt
    17701 aacaggccac aaataggcgt ggtaagagaa ttccttacac gtaaccctgc ttggagaaaa
    17761 gctgtcttta tttcacctta taattcacag aatgctgtag cctcaaagat tttgggacta
    17821 ccaactcaaa ctgttgattc atcacagggc tcagaatatg actatgtcat attcactcaa
    17881 accactgaaa cagctcactc ttgtaatgta aacagattta atgttgctat taccagagca
    17941 aaagtaggca tactttgcat aatgtctgat agagaccttt atgacaagtt gcaatttaca
    18001 agtcttgaaa ttccacgtag gaatgtggca actttacaag ctgaaaatgt aacaggactc
    18061 tttaaagatt gtagtaaggt aatcactggg ttacatccta cacaggcacc tacacacctc
    18121 agtgttgaca ctaaattcaa aactgaaggt ttatgtgttg acatacctgg catacctaag
    18181 gacatgacct atagaagact catctctatg atgggtttta aaatgaatta tcaagttaat
    18241 ggttacccta acatgtttat cacccgcgaa gaagctataa gacatgtacg tgcatggatt
    18301 ggcttcgatg tcgaggggtg tcatgctact agagaagctg ttggtaccaa tttaccttta
    18361 cagctaggtt tttctacagg tgttaaccta gttgctgtac ctacaggtta tgttgataca
    18421 cctaataata cagatttttc cagagttagt gctaaaccac cgcctggaga tcaatttaaa
    18481 cacctcatac cacttatgta caaaggactt ccttggaatg tagtgcgtat aaagattgta
    18541 caaatgttaa gtgacacact taaaaatctc tctgacagag tcgtatttgt cttatgggca
    18601 catggctttg agttgacatc tatgaagtat tttgtgaaaa taggacctga gcgcacctgt
    18661 tgtctatgtg atagacgtgc cacatgcttt tccactgctt cagacactta tgcctgttgg
    18721 catcattcta ttggatttga ttacgtctat aatccgttta tgattgatgt tcaacaatgg
    18781 ggttttacag gtaacctaca aagcaaccat gatctgtatt gtcaagtcca tggtaatgca
    18841 catgtagcta gttgtgatgc aatcatgact aggtgtctag ctgtccacga gtgctttgtt
    18901 aagcgtgttg actggactat tgaatatcct ataattggtg atgaactgaa gattaatgcg
    18961 gcttgtagaa aggttcaaca catggttgtt aaagctgcat tattagcaga caaattccca
    19021 gttcttcacg acattggtaa ccctaaagct attaagtgtg tacctcaagc tgatgtagaa
    19081 tggaagttct atgatgcaca gccttgtagt gacaaagctt ataaaataga agaattattc
    19141 tattcttatg ccacacattc tgacaaattc acagatggtg tatgcctatt ttggaattgc
    19201 aatgtcgata gatatcctgc taattccatt gtttgtagat ttgacactag agtgctatct
    19261 aaccttaact tgcctggttg tgatggtggc agtttgtatg taaataaaca tgcattccac
    19321 acaccagctt ttgataaaag tgcttttgtt aatttaaaac aattaccatt tttctattac
    19381 tctgacagtc catgtgagtc tcatggaaaa caagtagtgt cagatataga ttatgtacca
    19441 ctaaagtctg ctacgtgtat aacacgttgc aatttaggtg gtgctgtctg tagacatcat
    19501 gctaatgagt acagattgta tctcgatgct tataacatga tgatctcagc tggctttagc
    19561 ttgtgggttt acaaacaatt tgatacttat aacctctgga acacttttac aagacttcag
    19621 agtttagaaa atgtggcttt taatgttgta aataagggac actttgatgg acaacagggt
    19681 gaagtaccag tttctatcat taataacact gtttacacaa aagttgatgg tgttgatgta
    19741 gaattgtttg aaaataaaac aacattacct gttaatgtag catttgagct ttgggctaag
    19801 cgcaacatta aaccagtacc agaggtgaaa atactcaata atttgggtgt ggacattgct
    19861 gctaatactg tgatctggga ctacaaaaga gatgctccag cacatatatc tactattggt
    19921 gtttgttcta tgactgacat agccaagaaa ccaactgaaa cgatttgtgc accactcact
    19981 gtcttttttg atggtagagt tgatggtcaa gtagacttat ttagaaatgc ccgtaatggt
    20041 gttcttatta cagaaggtag tgttaaaggt ttacaaccat ctgtaggtcc caaacaagct
    20101 agtcttaatg gagtcacatt aattggagaa gccgtaaaaa cacagttcaa ttattataag
    20161 aaagttgatg gtgttgtcca acaattacct gaaacttact ttactcagag tagaaattta
    20221 caagaattta aacccaggag tcaaatggaa attgatttct tagaattagc tatggatgaa
    20281 ttcattgaac ggtataaatt agaaggctat gccttcgaac atatcgttta tggagatttt
    20341 agtcatagtc agttaggtgg tttacatcta ctgattggac tagctaaacg ttttaaggaa
    20401 tcaccttttg aattagaaga ttttattcct atggacagta cagttaaaaa ctatttcata
    20461 acagatgcgc aaacaggttc atctaagtgt gtgtgttctg ttattgattt attacttgat
    20521 gattttgttg aaataataaa atcccaagat ttatctgtag tttctaaggt tgtcaaagtg
    20581 actattgact atacagaaat ttcatttatg ctttggtgta aagatggcca tgtagaaaca
    20641 ttttacccaa aattacaatc tagtcaagcg tggcaaccgg gtgttgctat gcctaatctt
    20701 tacaaaatgc aaagaatgct attagaaaag tgtgaccttc aaaattatgg tgatagtgca
    20761 acattaccta aaggcataat gatgaatgtc gcaaaatata ctcaactgtg tcaatattta
    20821 aacacattaa cattagctgt accctataat atgagagtta tacattttgg tgctggttct
    20881 gataaaggag ttgcaccagg tacagctgtt ttaagacagt ggttgcctac gggtacgctg
    20941 cttgtcgatt cagatcttaa tgactttgtc tctgatgcag attcaacttt gattggtgat
    21001 tgtgcaactg tacatacagc taataaatgg gatctcatta ttagtgatat gtacgaccct
    21061 aagactaaaa atgttacaaa agaaaatgac tctaaagagg gttttttcac ttacatttgt
    21121 gggtttatac aacaaaagct agctcttgga ggttccgtgg ctataaagat aacagaacat
    21181 tcttggaatg ctgatcttta taagctcatg ggacacttcg catggtggac agcctttgtt
    21241 actaatgtga atgcgtcatc atctgaagca tttttaattg gatgtaatta tcttggcaaa
    21301 ccacgcgaac aaatagatgg ttatgtcatg catgcaaatt acatattttg gaggaataca
    21361 aatccaattc agttgtcttc ctattcttta tttgacatga gtaaatttcc ccttaaatta
    21421 aggggtactg ctgttatgtc tttaaaagaa ggtcaaatca atgatatgat tttatctctt
    21481 cttagtaaag gtagacttat aattagagaa aacaacagag ttgttatttc tagtgatgtt
    21541 cttgttaaca actaaacgaa caatgtttgt ttttcttgtt ttattgccac tagtctctag
    21601 tcagtgtgtt aatcttacaa ccagaactca attaccccct gcatacacta attctttcac
    21661 acgtggtgtt tattaccctg acaaagtttt cagatcctca gttttacatt caactcagga
    21721 cttgttctta cctttctttt ccaatgttac ttggttccat gctatacatg tctctgggac
    21781 caatggtact aagaggtttg ataaccctgt cctaccattt aatgatggtg tttattttgc
    21841 ttccactgag aagtctaaca taataagagg ctggattttt ggtactactt tagattcgaa
    21901 gacccagtcc ctacttattg ttaataacgc tactaatgtt gttattaaag tctgtgaatt
    21961 tcaattttgt aatgatccat ttttgggtgt ttattaccac aaaaacaaca aaagttggat
    22021 ggaaagtgag ttcagagttt attctagtgc gaataattgc acttttgaat atgtctctca
    22081 gccttttctt atggaccttg aaggaaaaca gggtaatttc aaaaatctta gggaatttgt
    22141 gtttaagaat attgatggtt attttaaaat atattctaag cacacgccta ttaatttagt
    22201 gcgtgatctc cctcagggtt tttcggcttt agaaccattg gtagatttgc caataggtat
    22261 taacatcact aggtttcaaa ctttacttgc tttacataga agttatttga ctcctggtga
    22321 ttcttcttca ggttggacag ctggtgctgc agcttattat gtgggttatc ttcaacctag
    22381 gacttttcta ttaaaatata atgaaaatgg aaccattaca gatgctgtag actgtgcact
    22441 tgaccctctc tcagaaacaa agtgtacgtt gaaatccttc actgtagaaa aaggaatcta
    22501 tcaaacttct aactttagag tccaaccaac agaatctatt gttagatttc ctaatattac
    22561 aaacttgtgc ccttttggtg aagtttttaa cgccaccaga tttgcatctg tttatgcttg
    22621 gaacaggaag agaatcagca actgtgttgc tgattattct gtcctatata attccgcatc
    22681 attttccact tttaagtgtt atggagtgtc tcctactaaa ttaaatgatc tctgctttac
    22741 taatgtctat gcagattcat ttgtaattag aggtgatgaa gtcagacaaa tcgctccagg
    22801 gcaaactgga aagattgctg attataatta taaattacca gatgatttta caggctgcgt
    22861 tatagcttgg aattctaaca atcttgattc taaggttggt ggtaattata attacctgta
    22921 tagattgttt aggaagtcta atctcaaacc ttttgagaga gatatttcaa ctgaaatcta
    22981 tcaggccggt agcacacctt gtaatggtgt tgaaggtttt aattgttact ttcctttaca
    23041 atcatatggt ttccaaccca ctaatggtgt tggttaccaa ccatacagag tagtagtact
    23101 ttcttttgaa cttctacatg caccagcaac tgtttgtgga cctaaaaagt ctactaattt
    23161 ggttaaaaac aaatgtgtca atttcaactt caatggttta acaggcacag gtgttcttac
    23221 tgagtctaac aaaaagtttc tgcctttcca acaatttggc agagacattg ctgacactac
    23281 tgatgctgtc cgtgatccac agacacttga gattcttgac attacaccat gttcttttgg
    23341 tggtgtcagt gttataacac caggaacaaa tacttctaac caggttgctg ttctttatca
    23401 ggatgttaac tgcacagaag tccctgttgc tattcatgca gatcaactta ctcctacttg
    23461 gcgtgtttat tctacaggtt ctaatgtttt tcaaacacgt gcaggctgtt taataggggc
    23521 tgaacatgtc aacaactcat atgagtgtga catacccatt ggtgcaggta tatgcgctag
    23581 ttatcagact cagactaatt ctcctcggcg ggcacgtagt gtagctagtc aatccatcat
    23641 tgcctacact atgtcacttg gtgcagaaaa ttcagttgct tactctaata actctattgc
    23701 catacccaca aattttacta ttagtgttac cacagaaatt ctaccagtgt ctatgaccaa
    23761 gacatcagta gattgtacaa tgtacatttg tggtgattca actgaatgca gcaatctttt
    23821 gttgcaatat ggcagttttt gtacacaatt aaaccgtgct ttaactggaa tagctgttga
    23881 acaagacaaa aacacccaag aagtttttgc acaagtcaaa caaatttaca aaacaccacc
    23941 aattaaagat tttggtggtt ttaatttttc acaaatatta ccagatccat caaaaccaag
    24001 caagaggtca tttattgaag atctactttt caacaaagtg acacttgcag atgctggctt
    24061 catcaaacaa tatggtgatt gccttggtga tattgctgct agagacctca tttgtgcaca
    24121 aaagtttaac ggccttactg ttttgccacc tttgctcaca gatgaaatga ttgctcaata
    24181 cacttctgca ctgttagcgg gtacaatcac ttctggttgg acctttggtg caggtgctgc
    24241 attacaaata ccatttgcta tgcaaatggc ttataggttt aatggtattg gagttacaca
    24301 gaatgttctc tatgagaacc aaaaattgat tgccaaccaa tttaatagtg ctattggcaa
    24361 aattcaagac tcactttctt ccacagcaag tgcacttgga aaacttcaag atgtggtcaa
    24421 ccaaaatgca caagctttaa acacgcttgt taaacaactt agctccaatt ttggtgcaat
    24481 ttcaagtgtt ttaaatgata tcctttcacg tcttgacaaa gttgaggctg aagtgcaaat
    24541 tgataggttg atcacaggca gacttcaaag tttgcagaca tatgtgactc aacaattaat
    24601 tagagctgca gaaatcagag cttctgctaa tcttgctgct actaaaatgt cagagtgtgt
    24661 acttggacaa tcaaaaagag ttgatttttg tggaaagggc tatcatctta tgtccttccc
    24721 tcagtcagca cctcatggtg tagtcttctt gcatgtgact tatgtccctg cacaagaaaa
    24781 gaacttcaca actgctcctg ccatttgtca tgatggaaaa gcacactttc ctcgtgaagg
    24841 tgtctttgtt tcaaatggca cacactggtt tgtaacacaa aggaattttt atgaaccaca
    24901 aatcattact acagacaaca catttgtgtc tggtaactgt gatgttgtaa taggaattgt
    24961 caacaacaca gtttatgatc ctttgcaacc tgaattagac tcattcaagg aggagttaga
    25021 taaatatttt aagaatcata catcaccaga tgttgattta ggtgacatct ctggcattaa
    25081 tgcttcagtt gtaaacattc aaaaagaaat tgaccgcctc aatgaggttg ccaagaattt
    25141 aaatgaatct ctcatcgatc tccaagaact tggaaagtat gagcagtata taaaatggcc
    25201 atggtacatt tggctaggtt ttatagctgg cttgattgcc atagtaatgg tgacaattat
    25261 gctttgctgt atgaccagtt gctgtagttg tctcaagggc tgttgttctt gtggatcctg
    25321 ctgcaaattt gatgaagacg actctgagcc agtgctcaaa ggagtcaaat tacattacac
    25381 ataaacgaac ttatggattt gtttatgaga atcttcacaa ttggaactgt aactttgaag
    25441 caaggtgaaa tcaaggatgc tactccttca gattttgttc gcgctactgc aacgataccg
    25501 atacaagcct cactcccttt cggatggctt attgttggcg ttgcacttct tgctgttttt
    25561 cagagcgctt ccaaaatcat aaccctcaaa aagagatggc aactagcact ctccaagggt
    25621 gttcactttg tttgcaactt gctgttgttg tttgtaacag tttactcaca ccttttgctc
    25681 gttgctgctg gccttgaagc cccttttctc tatctttatg ctttagtcta cttcttgcag
    25741 agtataaact ttgtaagaat aataatgagg ctttggcttt gctggaaatg ccgttccaaa
    25801 aacccattac tttatgatgc caactatttt ctttgctggc atactaattg ttacgactat
    25861 tgtatacctt acaatagtgt aacttcttca attgtcatta cttcaggtga tggcacaaca
    25921 agtcctattt ctgaacatga ctaccagatt ggtggttata ctgaaaaatg ggaatctgga
    25981 gtaaaagact gtgttgtatt acacagttac ttcacttcag actattacca gctgtactca
    26041 actcaattga gtacagacac tggtgttgaa catgttacct tcttcatcta caataaaatt
    26101 gttgatgagc ctgaagaaca tgtccaaatt cacacaatcg acggttcatc cggagttgtt
    26161 aatccagtaa tggaaccaat ttatgatgaa ccgacgacga ctactagcgt gcctttgtaa
    26221 gcacaagctg atgagtacga acttatgtac tcattcgttt cggaagagac aggtacgtta
    26281 atagttaata gcgtacttct ttttcttgct ttcgtggtat tcttgctagt tacactagcc
    26341 atccttactg cgcttcgatt gtgtgcgtac tgctgcaata ttgttaacgt gagtcttgta
    26401 aaaccttctt tttacgttta ctctcgtgtt aaaaatctga attcttctag agttcctgat
    26461 cttctggtct aaacgaacta aatattatat tagtttttct gtttggaact ttaattttag
    26521 ccatggcaga ttccaacggt actattaccg ttgaagagct taaaaagctc cttgaacaat
    26581 ggaacctagt aataggtttc ctattcctta catggatttg tcttctacaa tttgcctatg
    26641 ccaacaggaa taggtttttg tatataatta agttaatttt cctctggctg ttatggccag
    26701 taactttagc ttgttttgtg cttgctgctg tttacagaat aaattggatc accggtggaa
    26761 ttgctatcgc aatggcttgt cttgtaggct tgatgtggct cagctacttc attgcttctt
    26821 tcagactgtt tgcgcgtacg cgttccatgt ggtcattcaa tccagaaact aacattcttc
    26881 tcaacgtgcc actccatggc actattctga ccagaccgct tctagaaagt gaactcgtaa
    26941 tcggagctgt gatccttcgt ggacatcttc gtattgctgg acaccatcta ggacgctgtg
    27001 acatcaagga cctgcctaaa gaaatcactg ttgctacatc acgaacgctt tcttattaca
    27061 aattgggagc ttcgcagcgt gtagcaggtg actcaggttt tgctgcatac agtcgctaca
    27121 ggattggcaa ctataaatta aacacagacc attccagtag cagtgacaat attgctttgc
    27181 ttgtacagta agtgacaaca gatgtttcat ctcgttgact ttcaggttac tatagcagag
    27241 atattactaa ttattatgag gacttttaaa gtttccattt ggaatcttga ttacatcata
    27301 aacctcataa ttaaaaattt atctaagtca ctaactgaga ataaatattc tcaattagat
    27361 gaagagcaac caatggagat tgattaaacg aacatgaaaa ttattctttt cttggcactg
    27421 ataacactcg ctacttgtga gctttatcac taccaagagt gtgttagagg tacaacagta
    27481 cttttaaaag aaccttgctc ttctggaaca tacgagggca attcaccatt tcatcctcta
    27541 gctgataaca aatttgcact gacttgcttt agcactcaat ttgcttttgc ttgtcctgac
    27601 ggcgtaaaac acgtctatca gttacgtgcc agatcagttt cacctaaact gttcatcaga
    27661 caagaggaag ttcaagaact ttactctcca atttttctta ttgttgcggc aatagtgttt
    27721 ataacacttt gcttcacact caaaagaaag acagaatgat tgaactttca ttaattgact
    27781 tctatttgtg ctttttagcc tttctgctat tccttgtttt aattatgctt attatctttt
    27841 ggttctcact tgaactgcaa gatcataatg aaacttgtca cgcctaaacg aacatgaaat
    27901 ttcttgtttt cttaggaatc atcacaactg tagctgcatt tcaccaagaa tgtagtttac
    27961 agtcatgtac tcaacatcaa ccatatgtag ttgatgaccc gtgtcctatt cacttctatt
    28021 ctaaatggta tattagagta ggagctagaa aatcagcacc tttaattgaa ttgtgcgtgg
    28081 atgaggctgg ttctaaatca cccattcagt acatcgatat cggtaattat acagtttcct
    28141 gtttaccttt tacaattaat tgccaggaac ctaaattggg tagtcttgta gtgcgttgtt
    28201 cgttctatga agacttttta gagtatcatg acgttcgtgt tgttttagat ttcatctaaa
    28261 cgaacaaact aaaatgtctg ataatggacc ccaaaatcag cgaaatgcac cccgcattac
    28321 gtttggtgga ccctcagatt caactggcag taaccagaat ggagaacgca gtggggcgcg
    28381 atcaaaacaa cgtcggcccc aaggtttacc caataatact gcgtcttggt tcaccgctct
    28441 cactcaacat ggcaaggaag accttaaatt ccctcgagga caaggcgttc caattaacac
    28501 caatagcagt ccagatgacc aaattggcta ctaccgaaga gctaccagac gaattcgtgg
    28561 tggtgacggt aaaatgaaag atctcagtcc aagatggtat ttctactacc taggaactgg
    28621 gccagaagct ggacttccct atggtgctaa caaagacggc atcatatggg ttgcaactga
    28681 gggagccttg aatacaccaa aagatcacat tggcacccgc aatcctgcta acaatgctgc
    28741 aatcgtgcta caacttcctc aaggaacaac attgccaaaa ggcttctacg cagaagggag
    28801 cagaggcggc agtcaagcct cttctcgttc ctcatcacgt agtcgcaaca gttcaagaaa
    28861 ttcaactcca ggcagcagta ggggaacttc tcctgctaga atggctggca atggcggtga
    28921 tgctgctctt gctttgctgc tgcttgacag attgaaccag cttgagagca aaatgtctgg
    28981 taaaggccaa caacaacaag gccaaactgt cactaagaaa tctgctgctg aggcttctaa
    29041 gaagcctcgg caaaaacgta ctgccactaa agcatacaat gtaacacaag ctttcggcag
    29101 acgtggtcca gaacaaaccc aaggaaattt tggggaccag gaactaatca gacaaggaac
    29161 tgattacaaa cattggccgc aaattgcaca atttgccccc agcgcttcag cgttcttcgg
    29221 aatgtcgcgc attggcatgg aagtcacacc ttcgggaacg tggttgacct acacaggtgc
    29281 catcaaattg gatgacaaag atccaaattt caaagatcaa gtcattttgc tgaataagca
    29341 tattgacgca tacaaaacat tcccaccaac agagcctaaa aaggacaaaa agaagaaggc
    29401 tgatgaaact caagccttac cgcagagaca gaagaaacag caaactgtga ctcttcttcc
    29461 tgctgcagat ttggatgatt tctccaaaca attgcaacaa tccatgagca gtgctgactc
    29521 aactcaggcc taaactcatg cagaccacac aaggcagatg ggctatataa acgttttcgc
    29581 ttttccgttt acgatatata gtctactctt gtgcagaatg aattctcgta actacatagc
    29641 acaagtagat gtagttaact ttaatctcac atagcaatct ttaatcagtg tgtaacatta
    29701 gggaggactt gaaagagcca ccacattttc accgaggcca cgcggagtac gatcgagtgt
    29761 acagtgaaca atgctaggga gagctgccta tatggaagag ccctaatgtg taaaattaat
    29821 tttagtagtg ctatccccat gtgattttaa tagcttctta ggagaatgac aaaaaaaaaa
    29881 aaaaaaaaaa aaaaaaaaaa aaa"""


# > **This genome can be replaced in this notebook by saving it on the disk by creating a txt file and calling it like we've done in the next cell**

# In[ ]:


with open('../input/covid-genometxt/covid_genome.txt', 'r') as file:
    corona = file.read()


# In[ ]:


corona


# #### To remove all the numbers and spaces in the genome and just get the string of A, T, G, C. So using the replace function:

# In[ ]:


for a in " \n0123456789":
    corona = corona.replace(a, "")


# In[ ]:


corona


# #### Number of base pairs i.e. nucleotides in the modelule that made up the RNA and DNA

# In[ ]:


len(corona)


# # Kolmogorov complexity
# 
# #### Predicting the size of virus by compressing the genome of Corona virus. 'Kolmogorov complexity' (upperbounding because lower bounding is not possible). 

# #### Compressing using zlib 

# In[ ]:


import zlib
len(zlib.compress(corona.encode("utf-8")))
## for python 3 or more we need to utf-8 format encoding


# #### The above result means - The RNA of Coronavirus can contain '8858' bytes of information. This is just an upper-bound. This means - Coronavirus cannot contain more than '8858' bytes of information. Let's see if we can compress it a little more. HEre we used the zlib method of compression. We can look for better compression types like lzma.

# #### Compressing furthermore using lzma

# In[ ]:


import lzma
lzc = lzma.compress(corona.encode("utf-8"))
len(lzc)


# #### So, The RNA of Coronavirus can contain '8308' bytes of information. This is just an upper-bound. Hence it's a better compression way.

# # How to extract imformation from this genome information?
# 
# The genome contains the information about the proteins it can make. These proteins determine the characteristics of the cell in which they are produced. So we need to extract information about the proteins. To extract this info, we must know - how proteins are formed from the genetic material i.e. DNA/RNA.
# 
# > **Learning before applying:** RNAs and DNAs form proteins. This is how proteins are formed from DNA. In DNA, A-T/U and G-C form pairs. This pair formation is because - the chemical structure of A, T/U, G and C is such that - A and T are attracted towards each other by 2 hydrogen bonds and G and C together are attracted by 3 hydrogen bonds. A-C and G-T can't form such stable bonds. 
# 
# <img src="https://raw.githubusercontent.com/Bhard27/COVID-Genome-DS/master/images_copy/AT-GC.jpg" width="480">
# 
# <img src="https://raw.githubusercontent.com/Bhard27/COVID-Genome-DS/master/images_copy/codon2.png">
# 
# > What happens during protein formation is:
# 
# <img src="https://raw.githubusercontent.com/Bhard27/COVID-Genome-DS/master/images_copy/transcript-translate-cell.jpg">
# 
# <img src="https://raw.githubusercontent.com/Bhard27/COVID-Genome-DS/master/images_copy/codons.png">
# 
# > An enzyme called 'RNA polymerase' breaks these hydrogen bonds for a small part, takes one strand of DNA and forms its corresponding paired RNA. This process happens inside the nucleus of the cell. We call this RNA generated as 'mRNA' or 'messenger RNA' because this RNA will come out of nucleus and act like a messaage to Ribosome which will generate proteins accordingly. This process of generation of mRNA is called - **Transcription.** Now Ribosome will read the mRNA in sets of 3 bases. This set of 3 bases is called codon. Codons decide the Amino acids. Depending on the codon read by Ribosome, tRNA (transfer-RNA) brings the appropiate amino acid. These amino acids are then linked using peptide bonds to form a chain called *Polypeptide chain*. At the other end of Ribosome, tRNA is free and can go to take another amino acid. 
# 
# > *Note:* Amino acids are organic compounds that contain amine (-NH2) and carboxyl (-COOH) functional groups. There are 20 standard amino acids and 2 non-standard. Of the 20 standard amino acids, nine (His, Ile, Leu, Lys, Met, Phe, Thr, Trp and Val) are called essential amino acids because the human body cannot synthesize them from other compounds at the level needed for normal growth, so they must be obtained from food. Here is the table of codons and their corresponding Amino acids. 'Met' is usually the starting amino acid i.e. 'AUG' forms the start of mRNA. Hence 'AUG' is called *start codon.* 'UAA', 'UGA' and 'UAG' are *stop codons* as they mark the ending of the polypeptide chain, so that a new chain should start from the next codon. 
# 
# <img src=".https://raw.githubusercontent.com/Bhard27/COVID-Genome-DS/master/images_copy/genetic-code-table.jpg" width="600">
# 
# > This process of generation of chains of amino acids is called - **Translation.** A very long chain of amino acids is called *Protein.* In summary, we can understand the process as:
# 
# <img src="https://raw.githubusercontent.com/Bhard27/COVID-Genome-DS/master/images_copy/transcription-translation.png" width="600">
# 

# Now since in Coronavirus, we only has RNA, the process of Transcription won't occur and only Translation will happen. So what we now need to write is - *a translation function*, which takes corona's genome as input and gives back all the polypeptide chains that could be formed from that genome. For that, we first need a dictionary of codons. Following codons' string is copied from 'Genetic code' - Wikipedia. (https://en.wikipedia.org/wiki/DNA_codon_table)
# 
# <img src="./images_copy/codons.png">
# 

# In[ ]:


# Asn or Asp / B	AAU, AAC; GAU, GAC
# Gln or Glu / Z	CAA, CAG; GAA, GAG
# START	AUG
## Seperating them from the table because these duplicates was creating problems
codons = """
Ala / A	GCU, GCC, GCA, GCG
Ile / I	AUU, AUC, AUA
Arg / R	CGU, CGC, CGA, CGG; AGA, AGG, AGR;
Leu / L	CUU, CUC, CUA, CUG; UUA, UUG, UUR;
Asn / N	AAU, AAC
Lys / K	AAA, AAG
Asp / D	GAU, GAC
Met / M	AUG
Phe / F	UUU, UUC
Cys / C	UGU, UGC
Pro / P	CCU, CCC, CCA, CCG
Gln / Q	CAA, CAG
Ser / S	UCU, UCC, UCA, UCG; AGU, AGC;
Glu / E	GAA, GAG
Thr / T	ACU, ACC, ACA, ACG
Trp / W	UGG
Gly / G	GGU, GGC, GGA, GGG
Tyr / Y	UAU, UAC
His / H	CAU, CAC
Val / V	GUU, GUC, GUA, GUG
STOP	UAA, UGA, UAG""".strip()

for t in codons.split('\n'):
    print(t.split('\t'))


# > **To make this in a better readable format we'll making it into a decoder dictionary. Then making the decoder for DNA . We will also conevert the "U" to "T" in the list because the CoronaVIrus is a RNA virus and we will convert to DNA only dictionary.**

# In[ ]:


##decoder dictionary
dec = {}  

for t in codons.split('\n'):
    k, v = t.split('\t')
    if '/' in k:
        k = k.split('/')[-1].strip()
    k = k.replace("STOP", "*")
    v = v.replace(",", "").replace(";", "").lower().replace("u", "t").split(" ")
    for vv in v:
        if vv in dec:
            print("duplicate", vv)
        dec[vv] = k
dec


# ## We had to add the duplicate function because AUG is at multiple places, IT can bee seen in "Met" and in "Start" both. Which was creating problem in translation.

# In[ ]:


len(set(dec.values())) 


# > This means we have 21 amino acids in our decoder. Which can also be verified by the following chart, which shows there can be only 20 amino acids. Here we have a 'STOP' being the 21th amino acid. Which shows that the decoder works well.
#  
#  <img src="https://raw.githubusercontent.com/Bhard27/COVID-Genome-DS/master/images_copy/aminoproof.png">

# > Now, decoding the genome can result in one of the three possible ways. These 3 ways are called 'reading frames'. 
# 
# <img src="https://raw.githubusercontent.com/Bhard27/COVID-Genome-DS/master/images_copy/reading-frames.png" width="480">
# 
# In molecular biology, a reading frame is a way of dividing the sequence of nucleotides in a nucleic acid (DNA or RNA) molecule into a set of consecutive, non-overlapping triplets.

# In[ ]:


def translation(x, isProtein = False):
    aa = []
    for i in range(0, len(x)-2, 3):
        aa.append(dec[x[i:i+3]])
    aa = ''.join(aa)
    if isProtein:
        if aa[0] != "M" or aa[-1] != "*":
            print("BAD PROTEIN!")
            return None
        aa = aa[:-1]
    return aa

aa = translation(corona[0:]) + translation(corona[1:]) + translation(corona[2:])

##Refer to reading of codons for the above algorithm

aa


# # Polypeptides
# >In molecular biology, a reading frame is a way of dividing the sequence of nucleotides in a nucleic acid (DNA or RNA) molecule into a set of consecutive, non-overlapping triplets. Where these triplets equate to amino acids or stop signals during translation, they are called codons.
# 
# >A polypeptide is a longer, continuous, and unbranched peptide chain of up to fifty amino acids. Hence, peptides fall under the broad chemical classes of biological oligomers and polymers, alongside nucleic acids, oligosaccharides, polysaccharides, and others.
# 
# >When a polypeptide contains more than fifty amino acids it is known as a protein. Proteins consist of one or more polypeptides arranged in a biologically functional way, often bound to ligands such as coenzymes and cofactors, or to another protein or other macromolecule such as DNA or RNA, or to complex macromolecular assemblies.

# In[ ]:


polypeptides = aa.split("*")

polypeptides


# In[ ]:


len(polypeptides)


# In[ ]:


long_polypep_chains = list(filter(lambda x: len(x) > 100, aa.split("*")))

long_polypep_chains


# In[ ]:


len(long_polypep_chains)


# This is the genome organisation of Sars-Cov-2. _(Genome organisation is the linear order of genetic material (DNA/RNA) and its division into segments performing some specific function.)_ 
# 
# > Note: ORF stands for 'Open Reading Frame', the reading frame in which protein starts with M and ends with *.
# 
# Source: https://en.wikipedia.org/wiki/Severe_acute_respiratory_syndrome_coronavirus_2#Phylogenetics_and_taxonomy
# 
# <img src="https://raw.githubusercontent.com/Bhard27/COVID-Genome-DS/master/images_copy/SARS-CoV-2-genome.png" width="900">
# 
# Let's see if we can extract all the segments as mentioned here. We will refer to the following source again. Source: https://www.ncbi.nlm.nih.gov/nuccore/NC_045512
# 
# Also, if you will see the following genome organisation of Sars-Cov (old coronavirus), you will notice - the structure is very similar to Sars-CoV-2. _(Ignore the detailing given in the structure.)_
# 
# <img src="https://raw.githubusercontent.com/Bhard27/COVID-Genome-DS/master/images_copy/SARS-CoV-1-genome.png" width="800">

# In[ ]:


with open('../input/sarscov2/sars_cov2_genome.txt', 'r') as file:
    corona = file.read()

corona


# In[ ]:


for s in "\n01234567789 ":
    corona = corona.replace(s, "")


# In[ ]:


# https://www.ncbi.nlm.nih.gov/protein/1802476803 -  
# Orf1a polyprotein, found in Sars-Cov-2 (new Covid 19)
orf1a_poly_v2 = translation(corona[265:13483], True)

orf1a_poly_v2


# In[ ]:


# https://www.uniprot.org/uniprot/A7J8L3
# Orf1a polyprotein, found in Sars-Cov
with open('../input/proteins/orf1a.txt', 'r') as file:
    orf1a_poly_v1 = file.read().replace('\n', '')

orf1a_poly_v1


# In[ ]:


len(orf1a_poly_v1), len(orf1a_poly_v2)


# > Usually orf1b is not studied alone but along with orf1a. So we need to look at 'orf1ab'. But just to prove that the length of orf1b is 2595, here is just finding the length of orf1b in SARS-CoV-2.

# In[ ]:


# For orf1b_v1, refer - https://www.uniprot.org/uniprot/A0A0A0QGJ0
orf1a_poly_v2 = translation(corona[13467:21555])

# Length calculated from first 'M'. The last base is *, so extra -1 for that. 
len(orf1a_poly_v2) - orf1a_poly_v2.find('M') - 1  


# In[ ]:


# https://www.ncbi.nlm.nih.gov/protein/1796318597 - 
# Orf1ab polyprotein - found in Sars-cov-2
orf1a_poly_v2 = translation(corona[265:13468]) + translation(corona[13467:21555])


# In[ ]:


# https://www.uniprot.org/uniprot/A7J8L2
# Orf1ab polyprotein - found in Sars-cov

with open('../input/proteins/orf1ab.txt', 'r') as file:
    orf1a_poly_v2 = file.read().replace('\n', '')


# In[ ]:


len(orf1a_poly_v2), len(orf1a_poly_v1)


# > So by now, we have extracted Orf1a and Orf1b RNA segments.

# In[ ]:


# https://www.ncbi.nlm.nih.gov/protein/1796318598
# Spike glycoprotein - found in Sars-cov-2

spike_pro_v2 = translation(corona[21562:25384], True)

# https://www.ncbi.nlm.nih.gov/Structure/pdb/6VXX CLOSED FORM of glycoprotein (structure of glycoprotein before delivering the payload)
# https://www.ncbi.nlm.nih.gov/Structure/pdb/6VYB OPEN FORM of glycoprotein (structure of glycoprotein after delivering the payload)
spike_pro_v2


# In[ ]:


cn3 = open('../input/3d-structure/mmdb_6VXX.cn3', 'rb').read


# > Spike gylcoprotein is has catalystic properties which is responsible for attacking the body and multiplying the number of cells. The infection begins when the viral spike(S) glycoprotein attaches to it's compliementary host cell receptor, which usually is ACE2.

# In[ ]:


# https://www.uniprot.org/uniprot/P59594
# Spike glycoprotein - found in Sars-cov

with open('../input/proteins/spike.txt', 'r') as file:
    spike_v1 = file.read().replace('\n', '')


# In[ ]:


len(spike_pro_v2), len(spike_v1)


# In[ ]:


pip install nglview


# In[ ]:


import nglview
view = nglview.show_pdbid("6VXX")  # load "3pqr" from RCSB PDB and display viewer widget

view


# In[ ]:


import nglview
view = nglview.show_pdbid("6VYB")  # load "3pqr" from RCSB PDB and display viewer widget

view


# In[ ]:


# This whole thing has a "lipid" bi polar envelope" , with S E M. sticking out
# the orf proteins are "non structural" and form "replicable-transcriptae complex"

#copy machines -- https://www.uniprot.org/uniprot/Q0ZJN1
orf1a_poly_v1 = translation(corona[266-1:13483], True) 
orf1a_poly_v2 = translation(corona[13468-1:21555], False) 

# exploit vector, this attaches to ACE2 
spike_pro_v2 = translation(corona[21563-1:25384], True) 
orf3a_pro_v2 = translation(corona[25393-1:26220], True) 

# those two things stick out 
envelope_pro_v2 = translation(corona[26245-1:226472], True) 
membrane_pro_v2 = translation(corona[26523-1:27191], True) 

orf6_pro = translation(corona[27202-1:27387], True) 
orf7a_pro = translation(corona[27394-1:27759], True) 
orf7b_pro = translation(corona[27756-1:27887], True) 
orf8_pro = translation(corona[27894-1:28259], True) 
orf9_pro = translation(corona[28274-1:29533], True) 

len(corona)
                        


# In[ ]:


# https://www.ncbi.nlm.nih.gov/gene/43740569
# orf3a protein found in Sars-cov-2.

orf3a_pro_v2 = translation(corona[25392:26220], True)


# In[ ]:


# https://www.uniprot.org/uniprot/J9TEM7

with open('../input/proteins/orf3a.txt', 'r') as file:
    orf3a_pro_v1 = file.read().replace('\n', '')


# In[ ]:


len(orf3a_pro_v2), len(orf3a_pro_v1)


# By now we have observed that there is very little difference in the corresponding protein lengths of SARS-CoV and SARS-CoV-2.
# **So, Can we say that there isn't much difference between the proteins of two viruses?** Well, **Not Really** 
# 
# Reason for that is that the length of both the proteins is not the most accurate measure of how dissimilar they are. That arises a different question in front of us.
# 
# ### Q. 3 How much different is the protein of this novel coronavirus as compared to the older one?
# 
# The answer is - **The Edit Distance.** In computational linguistics and computer science, edit distance is a way of quantifying how dissimilar two strings (e.g., words) are to one another by counting the minimum number of operations required to transform one string into the other. In bioinformatics, it can be used to quantify the similarity of DNA sequences, which can be viewed as strings of the letters A, C, G and T. 
# 
# Source: https://en.wikipedia.org/wiki/Edit_distance
# 
# Let's calculate the edit distance of the genomes of the two versions of coronaviruses. 
# 
# Source of complete genome of old coronavirus: https://www.ncbi.nlm.nih.gov/nuccore/30271926

# In[ ]:


with open('../input/sarscov/sars_cov_genome.txt', 'r') as file:
    sars_cov = file.read()

print(sars_cov)


# In[ ]:


for s in "\n01234567789 ":
    sars_cov = sars_cov.replace(s, "")
    
sars_cov


# In[ ]:


import lzma
lzc_v1 = lzma.compress(sars_cov.encode("utf-8"))
len(lzc_v1)


# In[ ]:


len(lzc_v1) - len(lzc)


# In[ ]:


len(corona) - len(sars_cov)


# From this, we can see that - Novel coronavirus differ alot than expected from old coronavirus. Now that we know - the difference between two DNAs/RNAs is measured by calculating edit-distance, we can now just simply complete extracting other proteins. 

# > Cross verifying the length of Envelope protein as 75 aa

# In[ ]:


# https://www.ncbi.nlm.nih.gov/gene/43740570 - Envelope protein in Cov-2
envelope_pro_v2 = translation(corona[26244:26472], True)


# In[ ]:


len(envelope_pro_v2)


# > Cross verifying the length of Memberane protein which ia supposed to be 222aa

# In[ ]:


# https://www.ncbi.nlm.nih.gov/gene/43740571 - Membrane Glycoprotein in Cov-2
membrane_pro_v2 = translation(corona[26522:27191], True)


# In[ ]:


len(membrane_pro_v2)


# > Cross verifying the length of ORF6 protein which is supposed to be 61 aa

# In[ ]:


# https://www.ncbi.nlm.nih.gov/gene/43740572 - Orf6 in Cov-2
orf6_pro_v2 = translation(corona[27201:27387], True)


# In[ ]:


len(orf6_pro_v2)


# > Cross verifying the length of ORF7a protein which is supposed to be 121aa

# In[ ]:


# https://www.ncbi.nlm.nih.gov/gene/43740573 - orf7a in Cov-2
orf7a_pro = translation(corona[27393:27759], True)


# In[ ]:


len(orf7a_pro)


# > Cross verifying the length of ORF7b protein which is supposed to be 43aa

# In[ ]:


# https://www.ncbi.nlm.nih.gov/gene/43740574 - orf7b in Cov-2
orf7b_pro = translation(corona[27755:27887], True)


# In[ ]:


len(orf7b_pro)


# > Cross verifying the length of ORF8 protein which is supposed to be 121aa

# In[ ]:


# https://www.ncbi.nlm.nih.gov/gene/43740577 - orf8 in Cov-2
orf8_pro = translation(corona[27893:28259], True)


# In[ ]:


len(orf8_pro)


# > Cross verifying the length of ORF10 protein which is supposed to be 38aa

# In[ ]:


# https://www.ncbi.nlm.nih.gov/gene/43740576 - orf10 in Cov-2
orf10_pro = translation(corona[29557:29674], True)


# In[ ]:


len(orf10_pro)


# In[ ]:




