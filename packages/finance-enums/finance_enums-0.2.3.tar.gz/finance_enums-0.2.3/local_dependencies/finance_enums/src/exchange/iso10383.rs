use crate::CountryCode;
use serde::{Deserialize, Serialize};

#[derive(
    Copy, Clone, Debug, Deserialize, Display, EnumIter, EnumString, Eq, PartialEq, Serialize,
)]
#[strum(serialize_all = "PascalCase")]
pub enum MIC {
    /*################# NYSE #################*/
    XNYS, // NYSE
    NYSD, // NYSE Dark
    XCIS, // NYSE National
    CISD, // NYSE National Dark
    XCHI, // NYSE Chicago
    ARCX, // ARCA
    ARCD, // ARCA Dark
    ARCO, // ARCA Options
    XASE, // AMEX
    AMXO, // AMEX Options
    // XNLI, // NYSE LIFFE

    /*################# NASDAQ #################*/
    XNAS, // NASDAQ
    XNGS, // NASDAQ Global Select
    XNCM, // NASDAQ Capital Markets
    XNMS, // NASDAQ Global Market
    NASD, // NASDAQ Dark
    XNDQ, // NASDAQ Options
    XBOS, // NASDAQ Boston
    BOSD, // NASDAQ Boston Dark
    XBXO, // NASDAQ Boston Options
    XPHL, // NASDAQ Philly
    XPSX, // NASDAQ PSX (also philly?)
    PSXD, // NASDAQ Philly Dark
    XPHO, // NASDAQ Philly Options
    XPBT, // PBOT
    XPOR, // NASDAQ Portal
    // XBRT, // BRUT ECN
    XNFI, // NASDAQ Fixed Income
    XISE, // ISE Equities (ISE)
    GMNI, // ISE Gemini Options (GEMX)
    MCRY, // ISE Mercury Options (MRX)
    // XISA, // ISE Alternative Markets
    // XISX, // ISE

    /*################# CBOE #################*/
    XCBO, // CBOE
    EDGA, // EDGA
    EDGD, // EDGA DARK
    EDGX, // EDGX
    EDDP, // EDGX DARK
    EDGO, // EDGX Options
    BATS, // BZX
    BZXD, // BZX DARK
    BATO, // BZX Options
    BATY, // BYX
    BYXD, // BYX DARK
    C2OX, // CBOE C2 Options
    // BHSF, // CBOE Swap Execution Facility
    // HSFX, // CBOE Hotspot FX
    // XCBF, // CBOE Futures
    // XCBD, // CBOE Digital
    // CFIM, // CBOE Fixed Income

    /*################# CME #################*/
    XCME, // CME
    FCME, // CME Floor
    // XIMM, // CME IMM (FX / IR)
    GLBX, // Globex
    // XIOM, // CME INDEX AND OPTIONS MARKET
    // CMES, // CME SWAPS MARKETS (CME)
    // CBTS, // CME SWAPS MARKETS (CBOT)
    // NYMS, // CME SWAPS MARKETS (NYMEX)
    // CECS, // CME SWAPS MARKETS (COMEX)
    XCBT, // CBOT
    FCBT, // CBOT Floor
    XKBT, // KANSAS CITY BOARD OF TRADE
    XNYM, // NYMEX
    // XCEC, // NYMEX COMMODITIES EXCHANGE CENTER
    // XNYE, // NYMEX - OTC MARKETS
    // XNYL, // NYMEX - ENERGY MARKETS

    /*################# MIAX #################*/
    MIHI, // MIAX
    MPRL, // MIAX Pearl
    EPRL, // MIAX Pearl
    EPRD, // MIAX Pearl Dark
    XMIO, // MIAX Options
    EMLD, // MIAX Emerald Options

    /*################# OTC Markets #################*/
    OTCM, // OTC Markets
    CAVE, // OTC CAVEAT EMPTOR
    OTCB, // OTCQB MARKETPLACE
    OTCQ, // OTCQX MARKETPLACE
    PINL, // OTC PINK LIMITED
    PINI, // OTC PINK NO INFORMATION
    PINX, // OTC PINK MARKETPLACE
    PSGM, // OTC GREY MARKET
    PINC, // OTC PINK CURRENT

    /*################# FINRA #################*/
    FINR, // FINRA
    FINN, // FINRA NASDAQ TRF (NJ)
    FINC, // FINRA NASDAQ TRF (Chicago)
    FINY, // FINRA NYSE TRF
    XADF, // FINRA ADF
    FINO, // FINRA ORF
    OOTC, // Other OTC

    /*################# OTHER US #################*/
    OPRA, // OPRA
    MEMX, // MEMX
    MEMD, // MEMX Dark
    MXOP, // MEMX Options
    // MEMM,MEMX,SGMT,MEMX LLC RETAIL MIDPOINT,MEMX LLC,254900ZJZM9RSYHE7D79,NSPD,,US
    IEXG, // IEX
    // IEXD, // IEX Dark
    LTSE, // Long Term Stock Exchange

    /*################# Canadian Securities Exchange CSE #################*/
    XCNQ, // CSE
    PURE, // CSE Pure
    CSE2, // CSE CSE2

    /*################# TMX Group  #################*/
    XTSE, // TSE
    XDRK, // TSX Dark
    VDRK, // TSX Venture Dark
    XTSX, // TSX Venture
    XTNX, // TSX Venture Nex
    XATS, // Alpha Exchange
    XATX, // Alpha X
    ADRK, // Alpha Dark
    XMOD, // Montreal
    XMOC, // Montreal Climate

    /*################# CBOE NEO #################*/
    NEOE, // NEO Exchange
    NEOD, // NEO Exchange Dark
    NEON, // NEO Exchange (MARKET BY PRICE),,549300MILSKTNBLQ1L12,NSPD,NEO-N,CA,TORONTO,WWW.NEOSTOCKEXCHANGE.COM,ACTIVE,20180723,20190624,,,
    NEOC, // NEO Connect

    /*################# Other Canada / Canada ATS #################*/
    // XCX2,CHIC,SGMT,CX2,,,NSPD,,CA,TORONTO,WWW.CHI-X.COM/CA,ACTIVE
    // CHIC,CHIC,OPRT,CHI-X CANADA ATS,,,ATSS,,CA,TORONTO,WWW.CHI-XCANADA.COM,ACTIVE
    // EQCA,EQCA,OPRT,EQUILEND CANADA CORP.,EQUILEND CANADA CORP.,213800MJ9CY4JWO58S26,NSPD,,CA,TORONTO,WWW.EQUILEND.COM,ACTIVE
    // BNSX,BNSX,OPRT,THE BANK OF NOVA SCOTIA,,L3I9ZG2KFGXZ61BMYR72,SINT,,CA,TORONTO,WWW.SCOTIABANK.COM,ACTIVE
    // CAND,CAND,OPRT,CANDEAL.CA INC,,549300QSD4O4FEHPDA44,NSPD,CANDEAL,CA,TORONTO,WWW.CANDEAL.COM,ACTIVE
    // CANX,CANX,OPRT,CANNEX FINANCIAL EXCHANGE LTS,,,NSPD,CANNEX,CA,TORONTO,WWW.CANNEX.COM,ACTIVE
    // COTC,COTC,OPRT,BMO CAPITAL MARKETS - CAD OTC TRADES,,L64HM9LHPDOS1B9HJC68,NSPD,,CA,TORONTO,WWW.BMOCM.COM,ACTIVE
    // IVZX,IVZX,OPRT,INVESCO CANADA PTF TRADES,,9F443AVI6KXI3MYCLS29,NSPD,,CA,TORONTO,WWW.INVESCO.CA,ACTIVE
    // LICA,LICA,OPRT,LIQUIDNET CANADA ATS,,21380031335M4LHQJ436,ATSS,,CA,TORONTO,WWW.LIQUIDNET.COM,ACTIVE
    // MATN,MATN,OPRT,MATCH NOW,,,NSPD,,CA,TORONTO,WWW.TRIACTCANADA.COM,ACTIVE
    // NGXC,NGXC,OPRT,NATURAL GAS EXCHANGE,,549300MZWLT9C8T4VI12,NSPD,NGX,CA,CALGARY,WWW.NGX.COM,ACTIVE
    // OMGA,OMGA,OPRT,OMEGA ATS,,,ATSS,,CA,TORONTO,WWW.OMEGAATS.COM,ACTIVE
    // LYNX,OMGA,SGMT,LYNX ATS,,,ATSS,,CA,TORONTO,WWW.OMEGAATS.COM,ACTIVE
    // XBBK,XBBK,OPRT,PERIMETER FINANCIAL CORP. - BLOCKBOOK ATS,,,ATSS,,CA,TORONTO,WWW.PFIN.CA,ACTIVE
    // XCXD,XCXD,OPRT,NASDAQ CXD,,,NSPD,,CA,TORONTO,HTTP://BUSINESS.NASDAQ.COM/TRADE/CANADIAN-EQUITIES/OVERVIEW,ACTIVE
    // XICX,XICX,OPRT,INSTINET CANADA CROSS,,549300SU730FTQOKTE75,NSPD,,CA,TORONTO,WWW.INSTINET.COM,ACTIVE

    /*################# Other US based Equity ATS #################*/
    // https://www.finra.org/filing-reporting/otc-transparency/ats-equity-firms
    // https://www.sec.gov/foia/docs/atslist
    // ABEX, // 303 Alternatives LLC
    // BIDS, // Bids Trading LP
    // BNPC, // BNP Paribas Cortex
    // OCEA, // Blue Ocean ATS
    // CCMX, // Carta
    // ICBX, // Instinet
    // ONEC, // Citigroup One ATS
    // clearlist
    // CODA, // Coda Markets
    // CAES, // Credit Suisse Crossfinder
    // XSTM, // Fidelity Crossstream
    // dealerweb
    // EQX LLC
    // FNC AG STOCK
    // GOTC, // Global OTC
    // IATS, // Interactive Brokers ATS
    // IEOS, // Interactive Brokers EOS ATS
    // BAML, // BAML Instinct X ATS
    // INCR, // Intelligentcross ATS
    // INVESTX GEM
    // INX SECURITIES, LLC
    // JPBX, // JP Morgan Securities JPB-X
    // JPMX, // JP Morgan Securities JPM-X
    // LEVL, // Level ATS
    // LIUH, // Liquidnet H2O
    // LIQUIDNET NEGOTIATION ATS
    // lodas
    // LMNX, // Luminex ATS
    // MS POOL (ATS-4)	MSPL	MORGAN STANLEY & CO. LLC
    // MS RPOOL (ATS-6)	MSRP	MORGAN STANLEY & CO. LLC
    // MS TRAJECTORY CROSS (ATS-1)	MSTX	MORGAN STANLEY & CO. LLC
    // NFSTX, LLC	NFST	NFSTX, LLC
    // NORTH CAPITAL PRIVATE SECURITIES CORPORATION
    // OASIS PRO MARKETS LLC
    // CGXS, // ONECHRONOS
    // OTC Link
    // OTCN, // OTC Link ECN
    // OTCI, // OTC Link NQB IDQS
    // ITGI, // Virtu Posit
    // PROMETHEUM EMBER ATS INC.
    // STRM, // Purestream
    // SECURITIZE MARKETS ATS
    // SHARENETT ATS
    // SGMT, // Goldman Sigma X2
    // STARTENGINE SECONDARY
    // STFX, // Stifel, Nicolaus and Co STIFEL X ATS
    // TEXTURE ATS
    // BARX, // Barclays ATS
    // TOR ATS
    // UBSA, // UBS ATS
    // VARIABLE INVESTMENT ADVISORS, INC. ATS (VIAATS)
    // VCRS, // Virtu MATCHIT conditional room
    // VFMI, // Virtu Matchit
    // PJCX, // Piper Sandler and Co. ATS

    /*################# Other US based Options/Futures ATS #################*/
    // DASH, // DASH ATS
    // FNFT, // BGC Fenics Futures
    // BGCD, // BGC Derivatives
    // XBOX, // BOX

    /*################# Other US based Fixed Income ATS #################*/
    // https://www.finra.org/filing-reporting/otc-transparency/finra-equity-ats-firms-list
    // SCXA,SCXO,SGMT,SEED DIGITAL SECURITIES MARKET,,5493009JXYKN3NLOUE77,ATSS,,US
    // BNDS, // Bonds.com Bondspro
    // BTEQ, // BrokerTec
    // cboe fixed income (above)
    // CLARITY BIDRATE ALTERNATIVE TRADING SYSTEM
    // clearlist
    // CREDITMATCH
    // DWFI, // Dealerweb
    // FNCS, // BGCF Fenics
    // GSEF, // GFI Swaps Exchange
    // HTD-ATS
    // interactive broker ats (above)
    // ICSU, // ICAP SEF
    // VABD, // ICE Bondpoint
    // TMCC, // ICE TMC
    // IDXM, // IDX Markets
    // Kopen Tech Capital Markets
    // LESI, // LedgerEdge
    // LIFI, // Liquidnet Fixed Income ATS
    // MKAA, // Marketaxess ATS
    // LQED, // LIQUIDITYEDGE
    // MBS Source eTrading, Inc.
    // North Capital Private Securities Corporation
    // OASIS PRO MARKETS LLC
    // OTC Link (above)
    // SECURITIZE MARKETS ATS
    // SHARENETT ATS
    // TEXTURE ATS
    // TP ICAP Global Markets Americas LLC
    // TPCD, // TULLETT PREBON PLC - TP CREDITDEAL
    // BNDD, // TRADEWEB DIRECT
    // TRWB, // TRADEWEB LLC
    // TWSF,TRWB,SGMT,TW SEF LLC,,5493000G5QHJUY9ZWQ91,NSPD,TWSEF,US
    // DWSF,TRWB,SGMT,DW SEF LLC,,5493000G5QHJUY9ZWQ91,NSPD,DWSEF,US
    // TMID, // Trumid

    /*################# Other US based ATS #################*/
    // AATS, // Assent ATS
    // BLUE, // tZero / PRO SECURITIES ATS
    // CLST, // Clear Street
    // FNXB, // BGCF Fenicx Invitations
    // FNFX, // BGC Fenics FX
    // GFAM, // GFI
    // LATG, // GFI LATG
    // PRSE, // Pragma ATS
    // XAQS,XAQS,OPRT,AUTOMATED EQUITY FINANCE MARKETS,,,ATSS,AQS,US
    // XTXD, // XTX Direct

    /*################# US based options #################*/

    /*################# US based futures #################*/
    // SMFE, // Small Exchange

    /*################# US based fx #################*/

    /*################# US based crypto #################*/
    // BKKT, // BAKKT
    // FREX, // COINBASE DERIVATIVES
    // SFOX, // SFOX
    // XTRD, // XTRD

    /*################# OTHER PARENT ORGS #################*/
    // BGCF, // BGC Financial
    // BTEC, // ICAP Electronic Broking
    // GSCO, // Goldman Sachs
    // IBKR, // Interactive Brokers
    // JPMS, // JP Morgan Securities
    // LIUS, // Liquidnet US
    // MTXX, // Marketaxess
    // PIPR, // Piper Sandler and Co.
    // UBSS, // UBS Securities LLC
    // VUSA, // Virtu Americas
    // VFCM, // Virtu Financial Capital Markets
    // XTXM, // XTX Markets

    /*################# OTHER #################*/
    XXXX,

    /*################# NON ISO-10383 #################*/
    PYPR,
    SIMU,
}

impl MIC {
    pub fn operating_mic(&self) -> MIC {
        match self {
            /*################# NYSE #################*/
            MIC::XNYS => MIC::XNYS, // NYSE
            MIC::XCIS => MIC::XNYS, // NYSE National
            MIC::CISD => MIC::XNYS, // NYSE National Dark
            MIC::XCHI => MIC::XNYS, // NYSE Chicago
            MIC::ARCX => MIC::XNYS, // ARCA
            MIC::ARCD => MIC::XNYS, // ARCA Dark
            MIC::ARCO => MIC::XNYS, // ARCA Options
            MIC::XASE => MIC::XNYS, // AMEX
            MIC::AMXO => MIC::XNYS, // AMEX Options
            MIC::NYSD => MIC::XNYS, // NYSE Dark
            /*################# NASDAQ #################*/
            MIC::XNAS => MIC::XNAS, // NASDAQ
            MIC::XNGS => MIC::XNAS, // NASDAQ Global Select
            MIC::XNCM => MIC::XNAS, // NASDAQ Capital Markets
            MIC::XNMS => MIC::XNAS, // NASDAQ Global Market
            MIC::NASD => MIC::XNAS, // NASDAQ Dark
            MIC::XNDQ => MIC::XNAS, // NASDAQ Options
            MIC::XBOS => MIC::XNAS, // NASDAQ Boston
            MIC::BOSD => MIC::XNAS, // NASDAQ Boston Dark
            MIC::XBXO => MIC::XNAS, // NASDAQ Boston Options
            MIC::XPHL => MIC::XNAS, // NASDAQ Philly
            MIC::XPSX => MIC::XNAS, // NASDAQ PSX (also philly?)
            MIC::PSXD => MIC::XNAS, // NASDAQ Philly Dark
            MIC::XPHO => MIC::XNAS, // NASDAQ Philly Options
            MIC::XPBT => MIC::XNAS, // PBOT
            MIC::XPOR => MIC::XNAS, // NASDAQ Portal
            MIC::XNFI => MIC::XNAS, // NASDAQ Fixed Income
            MIC::XISE => MIC::XNAS, // ISE Equities (ISE)
            MIC::GMNI => MIC::XNAS, // ISE Gemini Options (GEMX)
            MIC::MCRY => MIC::XNAS, // ISE Mercury Options (MRX)
            // MIC::XISA => MIC::XNAS, // ISE Alternative Markets
            // MIC::XISX => MIC::XNAS, // ISE
            /*################# CBOE #################*/
            MIC::XCBO => MIC::XCBO, // CBOE
            MIC::EDGA => MIC::XCBO, // EDGA
            MIC::EDGD => MIC::XCBO, // EDGA DARK
            MIC::EDGX => MIC::XCBO, // EDGX
            MIC::EDDP => MIC::XCBO, // EDGX DARK
            MIC::EDGO => MIC::XCBO, // EDGX Options
            MIC::BATS => MIC::XCBO, // BZX
            MIC::BZXD => MIC::XCBO, // BZX DARK
            MIC::BATO => MIC::XCBO, // BZX Options
            MIC::BATY => MIC::XCBO, // BYX
            MIC::BYXD => MIC::XCBO, // BYX DARK
            MIC::C2OX => MIC::XCBO, // CBOE C2 Options
            // MIC::BHSF => MIC::XCBO, // CBOE Swap Execution Facility
            // MIC::HSFX => MIC::XCBO, // CBOE Hotspot FX
            // MIC::XCBF => MIC::XCBO, // CBOE Futures
            // MIC::XCBD => MIC::XCBO, // CBOE Digital
            // MIC::CFIM => MIC::XCBO, // CBOE Fixed Income

            /*################# CME #################*/
            MIC::XCME => MIC::XCME, // CME
            MIC::FCME => MIC::XCME, // CME Floor
            // MIC::XIMM => MIC::XCME, // CME IMM (FX / IR)
            MIC::GLBX => MIC::XCME, // Globex
            // MIC::XIOM => MIC::XCME, // CME INDEX AND OPTIONS MARKET,,,NSPD,IOM,US
            // MIC::CMES => MIC::XCME, // CME SWAPS MARKETS (CME)
            // MIC::CBTS => MIC::XCME, // CME SWAPS MARKETS (CBOT)
            // MIC::NYMS => MIC::XCME, // CME SWAPS MARKETS (NYMEX)
            // MIC::CECS => MIC::XCME, // CME SWAPS MARKETS (COMEX)
            MIC::XCBT => MIC::XCBT, // CBOT
            MIC::FCBT => MIC::XCBT, // CBOT Floor
            MIC::XKBT => MIC::XCBT, // KANSAS CITY BOARD OF TRADE
            MIC::XNYM => MIC::XNYM, // NYMEX
            // MIC::XCEC => MIC::XNYM, // NYMEX COMMODITIES EXCHANGE CENTER
            // MIC::XNYE => MIC::XNYM, // NYMEX - OTC MARKETS
            // MIC::XNYL => MIC::XNYM, // NYMEX - ENERGY MARKETS

            /*################# MIAX #################*/
            MIC::MIHI => MIC::MIHI, // MIAX
            MIC::MPRL => MIC::MIHI, // MIAX Pearl
            MIC::EPRL => MIC::MIHI, // MIAX Pearl
            MIC::EPRD => MIC::MIHI, // MIAX Pearl Dark
            MIC::XMIO => MIC::MIHI, // MIAX Options
            MIC::EMLD => MIC::MIHI, // MIAX Emerald Options

            /*################# OTC Markets #################*/
            MIC::OTCM => MIC::OTCM, // OTC Markets
            MIC::CAVE => MIC::OTCM, // OTC CAVEAT EMPTOR
            MIC::OTCB => MIC::OTCM, // OTCQB MARKETPLACE
            MIC::OTCQ => MIC::OTCM, // OTCQX MARKETPLACE
            MIC::PINL => MIC::OTCM, // OTC PINK LIMITED
            MIC::PINI => MIC::OTCM, // OTC PINK NO INFORMATION
            MIC::PINX => MIC::OTCM, // OTC PINK MARKETPLACE
            MIC::PSGM => MIC::OTCM, // OTC GREY MARKET
            MIC::PINC => MIC::OTCM, // OTC PINK CURRENT

            /*################# FINRA #################*/
            MIC::FINR => MIC::FINR, // FINRA
            MIC::FINN => MIC::FINR, // FINRA NASDAQ TRF (NJ)
            MIC::FINC => MIC::FINR, // FINRA NASDAQ TRF (Chicago)
            MIC::FINY => MIC::FINR, // FINRA NYSE TRF
            MIC::XADF => MIC::FINR, // FINRA ADF
            MIC::FINO => MIC::FINR, // FINRA ORF
            MIC::OOTC => MIC::FINR, // Other OTC

            /*################# OTHER US #################*/
            MIC::OPRA => MIC::OPRA, // OPRA
            MIC::MEMX => MIC::MEMX, // MEMX
            MIC::MEMD => MIC::MEMX, // MEMX Dark
            MIC::MXOP => MIC::MEMX, // MEMX Options
            MIC::IEXG => MIC::IEXG, // IEX
            MIC::LTSE => MIC::LTSE, // Long Term Stock Exchange

            /*################# Canadian Securities Exchange CSE #################*/
            MIC::XCNQ => MIC::XCNQ, // CSE
            MIC::PURE => MIC::XCNQ, // CSE Pure
            MIC::CSE2 => MIC::XCNQ, // CSE CSE2

            /*################# TMX Group  #################*/
            MIC::XTSE => MIC::XTSE, // TSE
            MIC::XDRK => MIC::XTSE, // TSX Dark
            MIC::XTSX => MIC::XTSX, // TSX Venture
            MIC::VDRK => MIC::XTSX, // TSX Venture Dark
            MIC::XTNX => MIC::XTSX, // TSX Venture Nex
            MIC::XATS => MIC::XATS, // Alpha Exchange
            MIC::XATX => MIC::XATS, // Alpha X
            MIC::ADRK => MIC::XATS, // Alpha Dark
            MIC::XMOD => MIC::XMOD, // Montreal
            MIC::XMOC => MIC::XMOD, // Montreal Climate

            /*################# CBOE NEO #################*/
            MIC::NEOE => MIC::NEOE, // NEO Exchange
            MIC::NEOD => MIC::NEOE, // NEO Exchange Dark
            MIC::NEON => MIC::NEOE, // NEO Exchange (MARKET BY PRICE),,549300MILSKTNBLQ1L12,NSPD,NEO-N,CA,TORONTO,WWW.NEOSTOCKEXCHANGE.COM,ACTIVE,20180723,20190624,,,
            MIC::NEOC => MIC::NEOE, // NEO Connect

            /*################# OTHER #################*/
            MIC::XXXX => MIC::XXXX,

            /*################# NON ISO-10383 #################*/
            MIC::PYPR => MIC::PYPR,
            MIC::SIMU => MIC::SIMU,
            // _ => MIC::XXXX, // Uncategorized
        }
    }

    pub fn name(&self) -> &'static str {
        match self {
            /*################# NYSE #################*/
            MIC::XNYS => "New York Stock Exchange",
            MIC::NYSD => "NYSE Dark",
            MIC::XCIS => "NYSE National",
            MIC::CISD => "NYSE National Dark",
            MIC::XCHI => "NYSE Chicago",
            MIC::ARCX => "NYSE ARCA",
            MIC::ARCD => "NYSE ARCA Dark",
            MIC::ARCO => "NYSE ARCA Options",
            MIC::XASE => "NYSE AMEX",
            MIC::AMXO => "NYSE AMEX Options",

            /*################# NASDAQ #################*/
            MIC::XNAS => "Nasdaq",
            MIC::XNGS => "Nasdaq Global Select",
            MIC::XNCM => "Nasdaq Capital Markets",
            MIC::XNMS => "Nasdaq Global Markets",
            MIC::NASD => "Nasdaq Dark",
            MIC::XNDQ => "Nasdaq Options",
            MIC::XBOS => "Nasdaq BX",
            MIC::BOSD => "Nasdaq BX Dark",
            MIC::XBXO => "Nasdaq BX Options",
            MIC::XPHL => "Nasdaq PHLX",
            MIC::XPSX => "Nasdaq PSX",
            MIC::PSXD => "Nasdaq PSX Dark",
            MIC::XPHO => "Nasdaq PSX Options",
            MIC::XPBT => "Philadelphia Board of Trade",
            MIC::XPOR => "Nasdaq Portal",
            MIC::XNFI => "Nasdaq Fixed Income",
            MIC::XISE => "ISE Equities",
            MIC::GMNI => "ISE Gemini Options",
            MIC::MCRY => "ISE Mercury Options",

            /*################# CBOE #################*/
            MIC::XCBO => "CBOE Global Markets",
            MIC::EDGA => "CBOE EDGA",
            MIC::EDGD => "CBOE EDGA Dark",
            MIC::EDGX => "CBOE EDGX",
            MIC::EDDP => "CBOE EDGX Dark",
            MIC::EDGO => "CBOE EDGX Options",
            MIC::BATS => "CBOE BZX",
            MIC::BZXD => "CBOE BZX Dark",
            MIC::BATO => "CBOE BZX Options",
            MIC::BATY => "CBOE BYX",
            MIC::BYXD => "CBOE BYX Dark",
            MIC::C2OX => "CBOE C2 Options",

            /*################# CME #################*/
            MIC::XCME => "Chicago Mercantile Exchange",
            MIC::FCME => "CME Floor",
            MIC::GLBX => "Globex",
            MIC::XCBT => "Chicago Board of Trade",
            MIC::FCBT => "CBOT Floor",
            MIC::XKBT => "Kansas City Board of Trade",
            MIC::XNYM => "New York Mercantile Exchange",

            /*################# MIAX #################*/
            MIC::MIHI => "MIAX",
            MIC::MPRL => "MIAX Pearl",
            MIC::EPRL => "MIAX Pearl",
            MIC::EPRD => "MIAX Pearl Dark",
            MIC::XMIO => "MIAX Options",
            MIC::EMLD => "MIAX Emerald",

            /*################# OTC Markets #################*/
            MIC::OTCM => "OTC Markets",
            MIC::CAVE => "OTC Caveat Emptor",
            MIC::OTCB => "OTC QB Marketplace",
            MIC::OTCQ => "OTC QX Marketplace",
            MIC::PINL => "OTC Pink Limited",
            MIC::PINI => "OTC Pink No Information",
            MIC::PINX => "OTC Pink Marketplace",
            MIC::PSGM => "OTC Grey Market",
            MIC::PINC => "OTC Pink Current",

            /*################# FINRA #################*/
            MIC::FINR => "FINRA",
            MIC::FINN => "FINRA NASDAQ TRF (NJ)",
            MIC::FINC => "FINRA NASDAQ TRF (Chicago)",
            MIC::FINY => "FINRA NYSE TRF",
            MIC::XADF => "FINRA ADF",
            MIC::FINO => "FINRA ORF",
            MIC::OOTC => "FINRA Other OTC",

            /*################# OTHER US #################*/
            MIC::OPRA => "Options Price Reporting Authority",
            MIC::MEMX => "Members Exchange",
            MIC::MEMD => "MEMX Dark",
            MIC::MXOP => "MEMX Options",
            MIC::IEXG => "Investors Exchange",
            MIC::LTSE => "Long-Term Stock Exchange",

            /*################# Canadian Securities Exchange CSE #################*/
            MIC::XCNQ => "Canadian Securities Exchange",
            MIC::PURE => "CSE Pure",
            MIC::CSE2 => "CSE CSE2",

            /*################# TMX Group  #################*/
            MIC::XTSE => "Toronto Stock Exchange",
            MIC::XDRK => "TSE Dark",
            MIC::XTSX => "TRX Venture Exchange",
            MIC::VDRK => "TRX Venture Exchange Dark",
            MIC::XTNX => "TRX Venture Nex",
            MIC::XATS => "Alpha Exchange",
            MIC::XATX => "Alpha Exchange X",
            MIC::ADRK => "Alpha Exchange Dark",
            MIC::XMOD => "Montréal Exchange",
            MIC::XMOC => "Montréal Climate Exchange",

            /*################# CBOE NEO #################*/
            MIC::NEOE => "NEO Exchange",
            MIC::NEOD => "NEO Exchange Dark",
            MIC::NEON => "NEO Exchange",
            MIC::NEOC => "NEO Connect",

            /*################# OTHER #################*/
            MIC::XXXX => "Uncategorized",

            /*################# NON ISO-10383 #################*/
            MIC::PYPR => "Paper",
            MIC::SIMU => "Simulation",
            // _ => "Uncategorized - Submit a Pull Request",
        }
    }

    pub fn country(&self) -> CountryCode {
        match self {
            // NYSE
            /*################# NYSE #################*/
            MIC::XNYS => CountryCode::US,
            MIC::NYSD => CountryCode::US,
            MIC::XCIS => CountryCode::US,
            MIC::CISD => CountryCode::US,
            MIC::XCHI => CountryCode::US,
            MIC::ARCX => CountryCode::US,
            MIC::ARCD => CountryCode::US,
            MIC::ARCO => CountryCode::US,
            MIC::XASE => CountryCode::US,
            MIC::AMXO => CountryCode::US,
            /*################# NASDAQ #################*/
            MIC::XNAS => CountryCode::US,
            MIC::XNGS => CountryCode::US,
            MIC::XNCM => CountryCode::US,
            MIC::XNMS => CountryCode::US,
            MIC::NASD => CountryCode::US,
            MIC::XNDQ => CountryCode::US,
            MIC::XBOS => CountryCode::US,
            MIC::BOSD => CountryCode::US,
            MIC::XBXO => CountryCode::US,
            MIC::XPHL => CountryCode::US,
            MIC::XPSX => CountryCode::US,
            MIC::PSXD => CountryCode::US,
            MIC::XPHO => CountryCode::US,
            MIC::XPBT => CountryCode::US,
            MIC::XPOR => CountryCode::US,
            MIC::XNFI => CountryCode::US,
            MIC::XISE => CountryCode::US,
            MIC::GMNI => CountryCode::US,
            MIC::MCRY => CountryCode::US,

            /*################# CBOE #################*/
            MIC::XCBO => CountryCode::US,
            MIC::EDGA => CountryCode::US,
            MIC::EDGD => CountryCode::US,
            MIC::EDGX => CountryCode::US,
            MIC::EDDP => CountryCode::US,
            MIC::EDGO => CountryCode::US,
            MIC::BATS => CountryCode::US,
            MIC::BZXD => CountryCode::US,
            MIC::BATO => CountryCode::US,
            MIC::BATY => CountryCode::US,
            MIC::BYXD => CountryCode::US,
            MIC::C2OX => CountryCode::US,

            /*################# CME #################*/
            MIC::XCME => CountryCode::US,
            MIC::FCME => CountryCode::US,
            MIC::GLBX => CountryCode::US,
            MIC::XCBT => CountryCode::US,
            MIC::FCBT => CountryCode::US,
            MIC::XKBT => CountryCode::US,
            MIC::XNYM => CountryCode::US,

            /*################# MIAX #################*/
            MIC::MIHI => CountryCode::US,
            MIC::MPRL => CountryCode::US,
            MIC::EPRL => CountryCode::US,
            MIC::EPRD => CountryCode::US,
            MIC::XMIO => CountryCode::US,
            MIC::EMLD => CountryCode::US,

            /*################# OTC Markets #################*/
            MIC::OTCM => CountryCode::US,
            MIC::CAVE => CountryCode::US,
            MIC::OTCB => CountryCode::US,
            MIC::OTCQ => CountryCode::US,
            MIC::PINL => CountryCode::US,
            MIC::PINI => CountryCode::US,
            MIC::PINX => CountryCode::US,
            MIC::PSGM => CountryCode::US,
            MIC::PINC => CountryCode::US,

            /*################# FINRA #################*/
            MIC::FINR => CountryCode::US,
            MIC::FINN => CountryCode::US,
            MIC::FINC => CountryCode::US,
            MIC::FINY => CountryCode::US,
            MIC::XADF => CountryCode::US,
            MIC::FINO => CountryCode::US,
            MIC::OOTC => CountryCode::US,

            /*################# OTHER US #################*/
            MIC::OPRA => CountryCode::US,
            MIC::MEMX => CountryCode::US,
            MIC::MEMD => CountryCode::US,
            MIC::MXOP => CountryCode::US,
            MIC::IEXG => CountryCode::US,
            MIC::LTSE => CountryCode::US,

            /*################# Canadian Securities Exchange CSE #################*/
            MIC::XCNQ => CountryCode::CA,
            MIC::PURE => CountryCode::CA,
            MIC::CSE2 => CountryCode::CA,

            /*################# TMX Group  #################*/
            MIC::XTSE => CountryCode::CA,
            MIC::XDRK => CountryCode::CA,
            MIC::XTSX => CountryCode::CA,
            MIC::VDRK => CountryCode::CA,
            MIC::XTNX => CountryCode::CA,
            MIC::XATS => CountryCode::CA,
            MIC::XATX => CountryCode::CA,
            MIC::ADRK => CountryCode::CA,
            MIC::XMOD => CountryCode::CA,
            MIC::XMOC => CountryCode::CA,

            /*################# CBOE NEO #################*/
            MIC::NEOE => CountryCode::CA,
            MIC::NEOD => CountryCode::CA,
            MIC::NEON => CountryCode::CA,
            MIC::NEOC => CountryCode::CA,

            /*################# OTHER #################*/
            MIC::XXXX => CountryCode::XX,

            /*################# NON ISO-10383 #################*/
            MIC::PYPR => CountryCode::XX,
            MIC::SIMU => CountryCode::XX,
            // _ => CountryCode::XX,
        }
    }
}
