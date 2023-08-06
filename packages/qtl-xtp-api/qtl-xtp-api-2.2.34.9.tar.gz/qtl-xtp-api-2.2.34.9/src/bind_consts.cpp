#include "bind_consts.h"


void bind_consts(nb::module_ &m) {
    nb::module_ consts = m.def_submodule("consts", "API Consts");

    consts.attr("XTP_LOG_LEVEL_FATAL") = 0;
    consts.attr("XTP_LOG_LEVEL_ERROR") = 1;
    consts.attr("XTP_LOG_LEVEL_WARNING") = 2;
    consts.attr("XTP_LOG_LEVEL_INFO") = 3;
    consts.attr("XTP_LOG_LEVEL_DEBUG") = 4;
    consts.attr("XTP_LOG_LEVEL_TRACE") = 5;

    consts.attr("XTP_PROTOCOL_TCP") = 1;
    consts.attr("XTP_PROTOCOL_UDP") = 2;

    consts.attr("XTP_EXCHANGE_SH") = 1;
    consts.attr("XTP_EXCHANGE_SZ") = 2;
    consts.attr("XTP_EXCHANGE_NQ") = 3;
    consts.attr("XTP_EXCHANGE_UNKNOWN") = 4;

    consts.attr("XTP_MKT_INIT") = 0;
    consts.attr("XTP_MKT_SZ_A") = 1;
    consts.attr("XTP_MKT_SH_A") = 2;
    consts.attr("XTP_MKT_BJ_A") = 3;
    consts.attr("XTP_MKT_HK") = 4;
    consts.attr("XTP_MKT_UNKNOWN") = 5;

    consts.attr("XTP_PRICE_LIMIT") = 1;
    consts.attr("XTP_PRICE_BEST_OR_CANCEL") = 2;
    consts.attr("XTP_PRICE_BEST5_OR_LIMIT") = 3;
    consts.attr("XTP_PRICE_BEST5_OR_CANCEL") = 4;
    consts.attr("XTP_PRICE_ALL_OR_CANCEL") = 5;
    consts.attr("XTP_PRICE_FORWARD_BEST") = 6;
    consts.attr("XTP_PRICE_REVERSE_BEST_LIMIT") = 7;
    consts.attr("XTP_PRICE_LIMIT_OR_CANCEL") = 8;
    consts.attr("XTP_PRICE_TYPE_UNKNOWN") = 9;

    consts.attr("XTP_SIDE_BUY") = 1;
    consts.attr("XTP_SIDE_SELL") = 2;
    consts.attr("XTP_SIDE_PURCHASE") = 7;
    consts.attr("XTP_SIDE_REDEMPTION") = 8;
    consts.attr("XTP_SIDE_SPLIT") = 9;
    consts.attr("XTP_SIDE_MERGE") = 10;
    consts.attr("XTP_SIDE_COVER") = 11;
    consts.attr("XTP_SIDE_FREEZE") = 12;
    consts.attr("XTP_SIDE_MARGIN_TRADE") = 21;
    consts.attr("XTP_SIDE_SHORT_SELL") = 22;
    consts.attr("XTP_SIDE_REPAY_MARGIN") = 23;
    consts.attr("XTP_SIDE_REPAY_STOCK") = 24;
    consts.attr("XTP_SIDE_STOCK_REPAY_STOCK") = 26;
    consts.attr("XTP_SIDE_SURSTK_TRANS") = 27;
    consts.attr("XTP_SIDE_GRTSTK_TRANSIN") = 28;
    consts.attr("XTP_SIDE_GRTSTK_TRANSOUT") = 29;
    consts.attr("XTP_SIDE_OPT_COMBINE") = 31;
    consts.attr("XTP_SIDE_OPT_SPLIT") = 32;
    consts.attr("XTP_SIDE_OPT_SPLIT_FORCE") = 33;
    consts.attr("XTP_SIDE_OPT_SPLIT_FORCE_EXCH") = 34;
    consts.attr("XTP_SIDE_UNKNOWN") = 50;

    consts.attr("XTP_POSITION_EFFECT_INIT") = 0;
    consts.attr("XTP_POSITION_EFFECT_OPEN") = 1;
    consts.attr("XTP_POSITION_EFFECT_CLOSE") = 2;
    consts.attr("XTP_POSITION_EFFECT_FORCECLOSE") = 3;
    consts.attr("XTP_POSITION_EFFECT_CLOSETODAY") = 4;
    consts.attr("XTP_POSITION_EFFECT_CLOSEYESTERDAY") = 5;
    consts.attr("XTP_POSITION_EFFECT_FORCEOFF") = 6;
    consts.attr("XTP_POSITION_EFFECT_LOCALFORCECLOSE") = 7;
    consts.attr("XTP_POSITION_EFFECT_CREDIT_FORCE_COVER") = 8;
    consts.attr("XTP_POSITION_EFFECT_CREDIT_FORCE_CLEAR") = 9;
    consts.attr("XTP_POSITION_EFFECT_CREDIT_FORCE_DEBT") = 10;
    consts.attr("XTP_POSITION_EFFECT_CREDIT_FORCE_UNCOND") = 11;
    consts.attr("XTP_POSITION_EFFECT_UNKNOWN") = 12;

    consts.attr("XTP_ORDER_ACTION_STATUS_SUBMITTED") = 1;
    consts.attr("XTP_ORDER_ACTION_STATUS_ACCEPTED") = 2;
    consts.attr("XTP_ORDER_ACTION_STATUS_REJECTED") = 3;

    consts.attr("XTP_ORDER_STATUS_INIT") = 0;
    consts.attr("XTP_ORDER_STATUS_ALLTRADED") = 1;
    consts.attr("XTP_ORDER_STATUS_PARTTRADEDQUEUEING") = 2;
    consts.attr("XTP_ORDER_STATUS_PARTTRADEDNOTQUEUEING") = 3;
    consts.attr("XTP_ORDER_STATUS_NOTRADEQUEUEING") = 4;
    consts.attr("XTP_ORDER_STATUS_CANCELED") = 5;
    consts.attr("XTP_ORDER_STATUS_REJECTED") = 6;
    consts.attr("XTP_ORDER_STATUS_UNKNOWN") = 7;

    consts.attr("XTP_ORDER_SUBMIT_STATUS_INSERT_SUBMITTED") = 1;
    consts.attr("XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED") = 2;
    consts.attr("XTP_ORDER_SUBMIT_STATUS_INSERT_REJECTED") = 3;
    consts.attr("XTP_ORDER_SUBMIT_STATUS_CANCEL_SUBMITTED") = 4;
    consts.attr("XTP_ORDER_SUBMIT_STATUS_CANCEL_REJECTED") = 5;
    consts.attr("XTP_ORDER_SUBMIT_STATUS_CANCEL_ACCEPTED") = 6;

    consts.attr("XTP_TERT_RESTART") = 0;
    consts.attr("XTP_TERT_RESUME") = 1;
    consts.attr("XTP_TERT_QUICK") = 2;

    consts.attr("ERT_CASH_FORBIDDEN") = 0;
    consts.attr("ERT_CASH_OPTIONAL") = 1;
    consts.attr("ERT_CASH_MUST") = 2;
    consts.attr("ERT_CASH_RECOMPUTE_INTER_SZ") = 3;
    consts.attr("ERT_CASH_MUST_INTER_SZ") = 4;
    consts.attr("ERT_CASH_RECOMPUTE_INTER_OTHER") = 5;
    consts.attr("ERT_CASH_MUST_INTER_OTHER") = 6;
    consts.attr("ERT_CASH_RECOMPUTE_INTER_HK") = 7;
    consts.attr("ERT_CASH_MUST_INTER_HK") = 8;
    consts.attr("EPT_INVALID") = 9;

    consts.attr("XTP_TICKER_TYPE_STOCK") = 0;
    consts.attr("XTP_TICKER_TYPE_INDEX") = 1;
    consts.attr("XTP_TICKER_TYPE_FUND") = 2;
    consts.attr("XTP_TICKER_TYPE_BOND") = 3;
    consts.attr("XTP_TICKER_TYPE_OPTION") = 4;
    consts.attr("XTP_TICKER_TYPE_TECH_STOCK") = 5;
    consts.attr("XTP_TICKER_TYPE_UNKNOWN") = 6;

    consts.attr("XTP_BUSINESS_TYPE_CASH") = 0;
    consts.attr("XTP_BUSINESS_TYPE_IPOS") = 1;
    consts.attr("XTP_BUSINESS_TYPE_REPO") = 2;
    consts.attr("XTP_BUSINESS_TYPE_ETF") = 3;
    consts.attr("XTP_BUSINESS_TYPE_MARGIN") = 4;
    consts.attr("XTP_BUSINESS_TYPE_DESIGNATION") = 5;
    consts.attr("XTP_BUSINESS_TYPE_ALLOTMENT") = 6;
    consts.attr("XTP_BUSINESS_TYPE_STRUCTURED_FUND_PURCHASE_REDEMPTION") = 7;
    consts.attr("XTP_BUSINESS_TYPE_STRUCTURED_FUND_SPLIT_MERGE") = 8;
    consts.attr("XTP_BUSINESS_TYPE_MONEY_FUND") = 9;
    consts.attr("XTP_BUSINESS_TYPE_OPTION") = 10;
    consts.attr("XTP_BUSINESS_TYPE_EXECUTE") = 11;
    consts.attr("XTP_BUSINESS_TYPE_FREEZE") = 12;
    consts.attr("XTP_BUSINESS_TYPE_OPTION_COMBINE") = 13;
    consts.attr("XTP_BUSINESS_TYPE_EXECUTE_COMBINE") = 14;
    consts.attr("XTP_BUSINESS_TYPE_UNKNOWN") = 15;

    consts.attr("XTP_ACCOUNT_NORMAL") = 0;
    consts.attr("XTP_ACCOUNT_CREDIT") = 1;
    consts.attr("XTP_ACCOUNT_DERIVE") = 2;
    consts.attr("XTP_ACCOUNT_UNKNOWN") = 3;

    consts.attr("XTP_FUND_TRANSFER_OUT") = 0;
    consts.attr("XTP_FUND_TRANSFER_IN") = 1;
    consts.attr("XTP_FUND_INTER_TRANSFER_OUT") = 2;
    consts.attr("XTP_FUND_INTER_TRANSFER_IN") = 3;
    consts.attr("XTP_FUND_INTER_TRANSFER_REPAY_OUT") = 4;
    consts.attr("XTP_FUND_INTER_TRANSFER_REPAY_IN") = 5;
    consts.attr("XTP_FUND_INTER_TRANSFER_CONTRACT_OUT") = 6;
    consts.attr("XTP_FUND_INTER_TRANSFER_CONTRACT_IN") = 7;
    consts.attr("XTP_FUND_TRANSFER_UNKNOWN") = 8;

    consts.attr("XTP_FUND_QUERY_JZ") = 0;
    consts.attr("XTP_FUND_QUERY_INTERNAL") = 1;
    consts.attr("XTP_FUND_QUERY_INTERNAL_REPAY") = 2;
    consts.attr("XTP_FUND_QUERY_INTERNAL_CONTRACT") = 3;
    consts.attr("XTP_FUND_QUERY_UNKNOWN") = 4;

    consts.attr("XTP_FUND_OPER_PROCESSING") = 0;
    consts.attr("XTP_FUND_OPER_SUCCESS") = 1;
    consts.attr("XTP_FUND_OPER_FAILED") = 2;
    consts.attr("XTP_FUND_OPER_SUBMITTED") = 3;
    consts.attr("XTP_FUND_OPER_UNKNOWN") = 4;

    consts.attr("XTP_DEBT_EXTEND_OPER_PROCESSING") = 0;
    consts.attr("XTP_DEBT_EXTEND_OPER_SUBMITTED") = 1;
    consts.attr("XTP_DEBT_EXTEND_OPER_SUCCESS") = 2;
    consts.attr("XTP_DEBT_EXTEND_OPER_FAILED") = 3;
    consts.attr("XTP_DEBT_EXTEND_OPER_UNKNOWN") = 4;

    consts.attr("XTP_SPLIT_MERGE_STATUS_ALLOW") = 0;
    consts.attr("XTP_SPLIT_MERGE_STATUS_ONLY_SPLIT") = 1;
    consts.attr("XTP_SPLIT_MERGE_STATUS_ONLY_MERGE") = 2;
    consts.attr("XTP_SPLIT_MERGE_STATUS_FORBIDDEN") = 3;

    consts.attr("XTP_TBT_ENTRUST") = 1;
    consts.attr("XTP_TBT_TRADE") = 2;
    consts.attr("XTP_TBT_STATE") = 3;

    consts.attr("XTP_QUOTE_REBUILD_UNKNOW") = 0;
    consts.attr("XTP_QUOTE_REBUILD_MD") = 1;
    consts.attr("XTP_QUOTE_REBUILD_TBT") = 2;

    consts.attr("XTP_REBUILD_RET_COMPLETE") = 1;
    consts.attr("XTP_REBUILD_RET_PARTLY") = 2;
    consts.attr("XTP_REBUILD_RET_NO_DATA") = 3;
    consts.attr("XTP_REBUILD_RET_PARAM_ERR") = 4;
    consts.attr("XTP_REBUILD_RET_FREQUENTLY") = 5;

    consts.attr("XTP_OPT_CALL") = 1;
    consts.attr("XTP_OPT_PUT") = 2;

    consts.attr("XTP_OPT_EXERCISE_TYPE_EUR") = 1;
    consts.attr("XTP_OPT_EXERCISE_TYPE_AME") = 2;

    consts.attr("XTP_POSITION_DIRECTION_NET") = 0;
    consts.attr("XTP_POSITION_DIRECTION_LONG") = 1;
    consts.attr("XTP_POSITION_DIRECTION_SHORT") = 2;
    consts.attr("XTP_POSITION_DIRECTION_COVERED") = 3;

    consts.attr("XTP_POSITION_UNCOVERED") = 0;
    consts.attr("XTP_POSITION_COVERED") = 1;

    consts.attr("XTP_CRD_CR_INIT") = 0;
    consts.attr("XTP_CRD_CR_SUCCESS") = 1;
    consts.attr("XTP_CRD_CR_FAILED") = 2;

    consts.attr("XTP_OPT_POSITION_TYPE_CONTRACT") = 0;
    consts.attr("XTP_OPT_POSITION_TYPE_COMBINED") = 1;

    consts.attr("XTP_ORDER_DETAIL_TYPE_NEW_ORDER") = 0;
    consts.attr("XTP_ORDER_DETAIL_TYPE_CANCEL_ORDER") = 1;
    consts.attr("XTP_ORDER_DETAIL_TYPE_OPT_COMB_NEW_ORDER") = 2;
    consts.attr("XTP_ORDER_DETAIL_TYPE_OPT_COMB_CANCEL_ORDER") = 3;

    consts.attr("XTP_TRDT_COMMON") = '0';
    consts.attr("XTP_TRDT_CASH") = '1';
    consts.attr("XTP_TRDT_PRIMARY") = '2';
    consts.attr("XTP_TRDT_CROSS_MKT_CASH") = '3';
    consts.attr("XTP_TRDT_HK_MKT_CASH") = '4';
    consts.attr("XTP_TRDT_NON_SHSZ_MKT_CASH") = '5';

    consts.attr("XTP_ORDT_Normal") = '0';
    consts.attr("XTP_ORDT_DeriveFromQuote") = '1';
    consts.attr("XTP_ORDT_DeriveFromCombination") = '2';
    consts.attr("XTP_ORDT_Combination") = '3';
    consts.attr("XTP_ORDT_ConditionalOrder") = '4';
    consts.attr("XTP_ORDT_Swap") = '5';

    consts.attr("XTP_TERMINAL_PC") = 1;
    consts.attr("XTP_TERMINAL_ANDROID") = 2;
    consts.attr("XTP_TERMINAL_IOS") = 3;
    consts.attr("XTP_TERMINAL_WP") = 4;
    consts.attr("XTP_TERMINAL_STATION") = 5;
    consts.attr("XTP_TERMINAL_TEL") = 6;
    consts.attr("XTP_TERMINAL_PC_LINUX") = 7;

    consts.attr("XTP_EXP_DATE_SAME") = 0;
    consts.attr("XTP_EXP_DATE_DIFF") = 1;
    consts.attr("XTP_EXP_DATE_NON") = 2;

    consts.attr("XTP_UNDERLYING_SAME") = 0;
    consts.attr("XTP_UNDERLYING_DIFF") = 1;
    consts.attr("XTP_UNDERLYING_NON") = 2;

    consts.attr("XTP_AUTO_SPLIT_EXPDAY") = 0;
    consts.attr("XTP_AUTO_SPLIT_PREDAY") = 1;
    consts.attr("XTP_AUTO_SPLIT_PRE2DAY") = 2;
    consts.attr("XTP_AUTO_SPLIT_NON") = 3;

    consts.attr("XTP_QUALIFICATION_PUBLIC") = 0;
    consts.attr("XTP_QUALIFICATION_COMMON") = 1;
    consts.attr("XTP_QUALIFICATION_ORGANIZATION") = 2;
    consts.attr("XTP_QUALIFICATION_UNKNOWN") = 3;

    consts.attr("XTP_SECURITY_MAIN_BOARD") = 0;
    consts.attr("XTP_SECURITY_SECOND_BOARD") = 1;
    consts.attr("XTP_SECURITY_STARTUP_BOARD") = 2;
    consts.attr("XTP_SECURITY_INDEX") = 3;
    consts.attr("XTP_SECURITY_TECH_BOARD") = 4;
    consts.attr("XTP_SECURITY_STATE_BOND") = 5;
    consts.attr("XTP_SECURITY_ENTERPRICE_BOND") = 6;
    consts.attr("XTP_SECURITY_COMPANEY_BOND") = 7;
    consts.attr("XTP_SECURITY_CONVERTABLE_BOND") = 8;
    consts.attr("XTP_SECURITY_NATIONAL_BOND_REVERSE_REPO") = 12;
    consts.attr("XTP_SECURITY_ETF_SINGLE_MARKET_STOCK") = 14;
    consts.attr("XTP_SECURITY_ETF_INTER_MARKET_STOCK") = 15;
    consts.attr("XTP_SECURITY_ETF_CROSS_BORDER_STOCK") = 16;
    consts.attr("XTP_SECURITY_ETF_SINGLE_MARKET_BOND") = 17;
    consts.attr("XTP_SECURITY_ETF_GOLD") = 19;
    consts.attr("XTP_SECURITY_STRUCTURED_FUND_CHILD") = 24;
    consts.attr("XTP_SECURITY_SZSE_RECREATION_FUND") = 26;
    consts.attr("XTP_SECURITY_STOCK_OPTION") = 29;
    consts.attr("XTP_SECURITY_ETF_OPTION") = 30;
    consts.attr("XTP_SECURITY_ALLOTMENT") = 100;
    consts.attr("XTP_SECURITY_MONETARY_FUND_SHCR") = 110;
    consts.attr("XTP_SECURITY_MONETARY_FUND_SHTR") = 111;
    consts.attr("XTP_SECURITY_MONETARY_FUND_SZ") = 112;
    consts.attr("XTP_SECURITY_OTHERS") = 255;

    consts.attr("XTP_POSITION_SECURITY_NORMAL") = 0;
    consts.attr("XTP_POSITION_SECURITY_PLACEMENT") = 1;
    consts.attr("XTP_POSITION_SECURITY_UNKNOWN") = 2;

    consts.attr("XTP_SECURITY_STATUS_ST") = 0;
    consts.attr("XTP_SECURITY_STATUS_N_IPO") = 1;
    consts.attr("XTP_SECURITY_STATUS_COMMON") = 2;
    consts.attr("XTP_SECURITY_STATUS_RESUME") = 3;
    consts.attr("XTP_SECURITY_STATUS_DELISTING") = 10;
    consts.attr("XTP_SECURITY_STATUS_OTHERS") = 255;

    consts.attr("XTP_TRADE_STATUS_UNKNOW") = 0;
    consts.attr("XTP_TRADE_STATUS_N") = 1;
    consts.attr("XTP_TRADE_STATUS_Y") = 2;
    consts.attr("XTP_TRADE_STATUS_D") = 3;
    consts.attr("XTP_TRADE_STATUS_I") = 4;
    consts.attr("XTP_TRADE_STATUS_F") = 5;

    consts.attr("XTP_SECURITY_LEVEL_UNKNOW") = 0;
    consts.attr("XTP_SECURITY_LEVEL_T") = 1;
    consts.attr("XTP_SECURITY_LEVEL_B") = 2;
    consts.attr("XTP_SECURITY_LEVEL_O") = 3;
    consts.attr("XTP_SECURITY_LEVEL_P") = 4;
    consts.attr("XTP_SECURITY_LEVEL_R") = 5;
    consts.attr("XTP_SECURITY_LEVEL_F") = 6;

    consts.attr("XTP_TRADE_TYPE_UNKNOW") = 0;
    consts.attr("XTP_TRADE_TYPE_T") = 1;
    consts.attr("XTP_TRADE_TYPE_M") = 2;
    consts.attr("XTP_TRADE_TYPE_B") = 3;
    consts.attr("XTP_TRADE_TYPE_C") = 4;
    consts.attr("XTP_TRADE_TYPE_P") = 5;
    consts.attr("XTP_TRADE_TYPE_O") = 6;

    consts.attr("XTP_SUSPEND_FLAG_UNKNOW") = 0;
    consts.attr("XTP_SUSPEND_FLAG_F") = 1;
    consts.attr("XTP_SUSPEND_FLAG_T") = 2;
    consts.attr("XTP_SUSPEND_FLAG_H") = 3;

    consts.attr("XTP_EX_DIVIDEND_FLAG_UNKNOW") = 0;
    consts.attr("XTP_EX_DIVIDEND_FLAG_N") = 1;
    consts.attr("XTP_EX_DIVIDEND_FLAG_E") = 2;
    consts.attr("XTP_EX_DIVIDEND_FLAG_D") = 3;
    consts.attr("XTP_EX_DIVIDEND_FLAG_A") = 4;

    // algo
    consts.attr("XTP_STRATEGY_STATE_CREATING") = 0;
    consts.attr("XTP_STRATEGY_STATE_CREATED") = 1;
    consts.attr("XTP_STRATEGY_STATE_STARTING") = 2;
    consts.attr("XTP_STRATEGY_STATE_STARTED") = 3;
    consts.attr("XTP_STRATEGY_STATE_STOPPING") = 4;
    consts.attr("XTP_STRATEGY_STATE_STOPPED") = 5;
    consts.attr("XTP_STRATEGY_STATE_DESTROYING") = 6;
    consts.attr("XTP_STRATEGY_STATE_DESTROYED") = 7;
    consts.attr("XTP_STRATEGY_STATE_ERROR") = 8;

}
