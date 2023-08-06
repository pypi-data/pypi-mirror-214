#ifndef TD_API_H
#define TD_API_H

#include <iostream>
#include <string>
#include <nanobind/nanobind.h>
#include <nanobind/trampoline.h>

#include "utils.h"
#include "dispatch_queue.h"
#include "xtp_trader_api.h"


namespace nb = nanobind;
namespace xtp = XTP::API;


class TdApi : public xtp::TraderSpi {
private:
    std::unique_ptr<DispatchQueue> queue_;
    xtp::TraderApi* api_;

public:
    void CreateTraderApi(int client_id, const std::string &save_file_path, int log_level);
    void Destroy();

    std::string GetTradingDay();
    std::string GetApiVersion();
    nb::dict GetApiLastError();

    uint8_t GetClientIDByXTPID(uint64_t order_xtp_id);
    std::string GetAccountByXTPID(uint64_t order_xtp_id);
    void SubscribePublicTopic(XTP_TE_RESUME_TYPE resume_type);
    void SetSoftwareVersion(const char* version);
    void SetSoftwareKey(const char* key);
    void SetHeartBeatInterval(uint32_t interval);
    uint64_t Login(const char* ip, int port, const char* user, const char* password, XTP_PROTOCOL_TYPE sock_type, const char* local_ip = NULL);
    int Logout(uint64_t session_id);
    bool IsServerRestart(uint64_t session_id);
    int ModifyUserTerminalInfo(const nb::dict &info, uint64_t session_id);
    int QueryAccountTradeMarket(uint64_t session_id, int request_id);
    uint64_t GetANewOrderXTPID(uint64_t session_id);
    uint64_t InsertOrder(const nb::dict &order, uint64_t session_id);
    uint64_t InsertOrderExtra(const nb::dict &order, uint64_t session_id);
    uint64_t CancelOrder(const uint64_t order_xtp_id, uint64_t session_id);
    int QueryOrderByXTPID(const uint64_t order_xtp_id, uint64_t session_id, int request_id);
    int QueryOrders(const nb::dict &query_param, uint64_t session_id, int request_id);
    int QueryUnfinishedOrders(uint64_t session_id, int request_id);
    int QueryOrdersByPage(const nb::dict &query_param, uint64_t session_id, int request_id);
    int QueryOrderByXTPIDEx(const uint64_t order_xtp_id, uint64_t session_id, int request_id);
    int QueryOrdersEx(const nb::dict &query_param, uint64_t session_id, int request_id);
    int QueryUnfinishedOrdersEx(uint64_t session_id, int request_id);
    int QueryOrdersByPageEx(const nb::dict &query_param, uint64_t session_id, int request_id);
    int QueryTradesByXTPID(const uint64_t order_xtp_id, uint64_t session_id, int request_id);
    int QueryTrades(const nb::dict &query_param, uint64_t session_id, int request_id);
    int QueryTradesByPage(const nb::dict &query_param, uint64_t session_id, int request_id);
    int QueryPosition(const char *ticker, uint64_t session_id, int request_id, XTP_MARKET_TYPE market = XTP_MKT_INIT);
    int QueryAsset(uint64_t session_id, int request_id);
    int QueryStructuredFund(const nb::dict &query_param, uint64_t session_id, int request_id);
    uint64_t FundTransfer(const nb::dict &fund_transfer, uint64_t session_id);
    int QueryFundTransfer(const nb::dict &query_param, uint64_t session_id, int request_id);
    int QueryOtherServerFund(const nb::dict &query_param, uint64_t session_id, int request_id);
    int QueryETF(const nb::dict &query_param, uint64_t session_id, int request_id);
    int QueryETFTickerBasket(const nb::dict &query_param, uint64_t session_id, int request_id);
    int QueryIPOInfoList(uint64_t session_id, int request_id);
    int QueryIPOQuotaInfo(uint64_t session_id, int request_id);
    int QueryOptionAuctionInfo(const nb::dict &query_param, uint64_t session_id, int request_id);
    uint64_t CreditCashRepay(double amount, uint64_t session_id);
    uint64_t CreditCashRepayDebtInterestFee(const char* debt_id, double amount, uint64_t session_id);
    uint64_t CreditSellStockRepayDebtInterestFee(const nb::dict &order, const char* debt_id, uint64_t session_id);
    int QueryCreditCashRepayInfo(uint64_t session_id, int request_id);
    int QueryCreditFundInfo(uint64_t session_id, int request_id);
    int QueryCreditDebtInfo(uint64_t session_id, int request_id);
    int QueryCreditTickerDebtInfo(const nb::dict &query_param, uint64_t session_id, int request_id);
    int QueryCreditAssetDebtInfo(uint64_t session_id, int request_id);
    int QueryCreditTickerAssignInfo(const nb::dict &query_param, uint64_t session_id, int request_id);
    int QueryCreditExcessStock(const nb::dict &query_param, uint64_t session_id, int request_id);
    int QueryMulCreditExcessStock(const nb::dict &query_param, uint64_t session_id, int request_id);
    uint64_t CreditExtendDebtDate(const nb::dict &debt_extend, uint64_t session_id);
    int QueryCreditExtendDebtDateOrders(uint64_t xtp_id, uint64_t session_id, int request_id);
    int QueryCreditFundExtraInfo(uint64_t session_id, int request_id);
    int QueryCreditPositionExtraInfo(const nb::dict &query_param, uint64_t session_id, int request_id);
    uint64_t InsertOptionCombinedOrder(const nb::dict &order, uint64_t session_id);
    uint64_t InsertOptionCombinedOrderExtra(const nb::dict &order, uint64_t session_id);
    uint64_t CancelOptionCombinedOrder(const uint64_t order_xtp_id, uint64_t session_id);
    int QueryOptionCombinedUnfinishedOrders(uint64_t session_id, int request_id);
    int QueryOptionCombinedOrderByXTPID(const uint64_t order_xtp_id, uint64_t session_id, int request_id);
    int QueryOptionCombinedOrders(const nb::dict &query_param, uint64_t session_id, int request_id);
    int QueryOptionCombinedOrdersByPage(const nb::dict &query_param, uint64_t session_id, int request_id);
    int QueryOptionCombinedUnfinishedOrdersEx(uint64_t session_id, int request_id);
    int QueryOptionCombinedOrderByXTPIDEx(const uint64_t order_xtp_id, uint64_t session_id, int request_id);
    int QueryOptionCombinedOrdersEx(const nb::dict &query_param, uint64_t session_id, int request_id);
    int QueryOptionCombinedOrdersByPageEx(const nb::dict &query_param, uint64_t session_id, int request_id);
    int QueryOptionCombinedTradesByXTPID(const uint64_t order_xtp_id, uint64_t session_id, int request_id);
    int QueryOptionCombinedTrades(const nb::dict &query_param, uint64_t session_id, int request_id);
    int QueryOptionCombinedTradesByPage(const nb::dict &query_param, uint64_t session_id, int request_id);
    int QueryOptionCombinedPosition(const nb::dict &query_param, uint64_t session_id, int request_id);
    int QueryOptionCombinedStrategyInfo(uint64_t session_id, int request_id);
    int QueryOptionCombinedExecPosition(const nb::dict &query_param, uint64_t session_id, int request_id);
    int LoginALGO(const char* ip, int port, const char* user, const char* password, XTP_PROTOCOL_TYPE sock_type, const char* local_ip = NULL);
    int QueryStrategy(uint32_t strategy_type, uint64_t client_strategy_id, uint64_t xtp_strategy_id, uint64_t session_id, int32_t request_id);
    int ALGOUserEstablishChannel(const char* oms_ip, int oms_port, const char* user, const char* password, uint64_t session_id);
    int InsertAlgoOrder(uint32_t strategy_type, uint64_t client_strategy_id, const char* strategy_param, uint64_t session_id);
    int CancelAlgoOrder(bool cancel_flag, uint64_t xtp_strategy_id, uint64_t session_id);
    uint64_t GetAlgorithmIDByOrder(uint64_t order_xtp_id, uint32_t order_client_id);
    int StrategyRecommendation(bool basket_flag, const char* basket_param, uint64_t session_id, int32_t request_id);

    void OnDisconnected(uint64_t session_id, int reason) override;
    void OnError(XTPRI *error_info) override;
    void OnQueryAccountTradeMarket(int trade_location, XTPRI *error_info, int request_id, uint64_t session_id) override;
    void OnOrderEvent(XTPOrderInfo *order_info, XTPRI *error_info, uint64_t session_id) override;
    void OnTradeEvent(XTPTradeReport *trade_info, uint64_t session_id) override;
    void OnCancelOrderError(XTPOrderCancelInfo *cancel_info, XTPRI *error_info, uint64_t session_id) override;
    void OnQueryOrder(XTPQueryOrderRsp *order_info, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) override;
    void OnQueryOrderEx(XTPOrderInfoEx *order_info, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) override;
    void OnQueryOrderByPage(XTPQueryOrderRsp *order_info, int64_t req_count, int64_t order_sequence, int64_t query_reference, int request_id, bool is_last, uint64_t session_id) override;
    void OnQueryOrderByPageEx(XTPOrderInfoEx *order_info, int64_t req_count, int64_t order_sequence, int64_t query_reference, int request_id, bool is_last, uint64_t session_id) override;
    void OnQueryTrade(XTPQueryTradeRsp *trade_info, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) override;
    void OnQueryTradeByPage(XTPQueryTradeRsp *trade_info, int64_t req_count, int64_t trade_sequence, int64_t query_reference, int request_id, bool is_last, uint64_t session_id) override;
    void OnQueryPosition(XTPQueryStkPositionRsp *position, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) override;
    void OnQueryAsset(XTPQueryAssetRsp *asset, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) override;
    void OnQueryStructuredFund(XTPStructuredFundInfo *fund_info, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) override;
    void OnQueryFundTransfer(XTPFundTransferNotice *fund_transfer_info, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) override;
    void OnFundTransfer(XTPFundTransferNotice *fund_transfer_info, XTPRI *error_info, uint64_t session_id) override;
    void OnQueryOtherServerFund(XTPFundQueryRsp *fund_info, XTPRI *error_info, int request_id, uint64_t session_id) override;
    void OnQueryETF(XTPQueryETFBaseRsp *etf_info, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) override;
    void OnQueryETFBasket(XTPQueryETFComponentRsp *etf_component_info, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) override;
    void OnQueryIPOInfoList(XTPQueryIPOTickerRsp *ipo_info, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) override;
    void OnQueryIPOQuotaInfo(XTPQueryIPOQuotaRsp *quota_info, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) override;
    void OnQueryOptionAuctionInfo(XTPQueryOptionAuctionInfoRsp *option_info, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) override;
    void OnCreditCashRepay(XTPCrdCashRepayRsp *cash_repay_info, XTPRI *error_info, uint64_t session_id) override;
    void OnCreditCashRepayDebtInterestFee(XTPCrdCashRepayDebtInterestFeeRsp *cash_repay_info, XTPRI *error_info, uint64_t session_id) override;
    void OnQueryCreditCashRepayInfo(XTPCrdCashRepayInfo *cash_repay_info, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) override;
    void OnQueryCreditFundInfo(XTPCrdFundInfo *fund_info, XTPRI *error_info, int request_id, uint64_t session_id) override;
    void OnQueryCreditDebtInfo(XTPCrdDebtInfo *debt_info, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) override;
    void OnQueryCreditTickerDebtInfo(XTPCrdDebtStockInfo *debt_info, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) override;
    void OnQueryCreditAssetDebtInfo(double remain_amount, XTPRI *error_info, int request_id, uint64_t session_id) override;
    void OnQueryCreditTickerAssignInfo(XTPClientQueryCrdPositionStkInfo *assign_info, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) override;
    void OnQueryCreditExcessStock(XTPClientQueryCrdSurplusStkRspInfo* stock_info, XTPRI *error_info, int request_id, uint64_t session_id) override;
    void OnQueryMulCreditExcessStock(XTPClientQueryCrdSurplusStkRspInfo* stock_info, XTPRI *error_info, int request_id, uint64_t session_id, bool is_last) override;
    void OnCreditExtendDebtDate(XTPCreditDebtExtendNotice *debt_extend_info, XTPRI *error_info, uint64_t session_id) override;
    void OnQueryCreditExtendDebtDateOrders(XTPCreditDebtExtendNotice *debt_extend_info, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) override;
    void OnQueryCreditFundExtraInfo(XTPCrdFundExtraInfo *fund_info, XTPRI *error_info, int request_id, uint64_t session_id) override;
    void OnQueryCreditPositionExtraInfo(XTPCrdPositionExtraInfo *fund_info, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) override;
    void OnOptionCombinedOrderEvent(XTPOptCombOrderInfo *order_info, XTPRI *error_info, uint64_t session_id) override;
    void OnOptionCombinedTradeEvent(XTPOptCombTradeReport *trade_info, uint64_t session_id) override;
    void OnCancelOptionCombinedOrderError(XTPOptCombOrderCancelInfo *cancel_info, XTPRI *error_info, uint64_t session_id) override;
    void OnQueryOptionCombinedOrders(XTPQueryOptCombOrderRsp *order_info, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) override;
    void OnQueryOptionCombinedOrdersEx(XTPOptCombOrderInfoEx *order_info, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) override;
    void OnQueryOptionCombinedOrdersByPage(XTPQueryOptCombOrderRsp *order_info, int64_t req_count, int64_t order_sequence, int64_t query_reference, int request_id, bool is_last, uint64_t session_id) override;
    void OnQueryOptionCombinedOrdersByPageEx(XTPOptCombOrderInfoEx *order_info, int64_t req_count, int64_t order_sequence, int64_t query_reference, int request_id, bool is_last, uint64_t session_id) override;
    void OnQueryOptionCombinedTrades(XTPQueryOptCombTradeRsp *trade_info, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) override;
    void OnQueryOptionCombinedTradesByPage(XTPQueryOptCombTradeRsp *trade_info, int64_t req_count, int64_t trade_sequence, int64_t query_reference, int request_id, bool is_last, uint64_t session_id) override;
    void OnQueryOptionCombinedPosition(XTPQueryOptCombPositionRsp *position_info, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) override;
    void OnQueryOptionCombinedStrategyInfo(XTPQueryCombineStrategyInfoRsp *strategy_info, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) override;
    void OnQueryOptionCombinedExecPosition(XTPQueryOptCombExecPosRsp *position_info, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) override;
    void OnQueryStrategy(XTPStrategyInfoStruct* strategy_info, char* strategy_param, XTPRI *error_info, int32_t request_id, bool is_last, uint64_t session_id) override;
    void OnStrategyStateReport(XTPStrategyStateReportStruct* strategy_state, uint64_t session_id) override;
    void OnALGOUserEstablishChannel(char* user, XTPRI* error_info, uint64_t session_id) override;
    void OnInsertAlgoOrder(XTPStrategyInfoStruct* strategy_info, XTPRI *error_info, uint64_t session_id) override;
    void OnCancelAlgoOrder(XTPStrategyInfoStruct* strategy_info, XTPRI *error_info, uint64_t session_id) override;
    void OnAlgoDisconnected(int reason) override;
    void OnAlgoConnected() override;
    void OnStrategySymbolStateReport(XTPStrategySymbolStateReport* strategy_symbol_state, uint64_t session_id) override;
    void OnNewStrategyCreateReport(XTPStrategyInfoStruct* strategy_info, char* strategy_param, uint64_t session_id) override;
    void OnStrategyRecommendation(bool basket_flag, XTPStrategyRecommendationInfo* recommendation_info, char* strategy_param, XTPRI *error_info, int32_t request_id, bool is_last, uint64_t session_id) override;

    virtual void PyOnDisconnected(uint64_t session_id, int reason) = 0;
    virtual void PyOnError(const nb::dict &error_info) = 0;
    virtual void PyOnQueryAccountTradeMarket(int trade_location, const nb::dict &error_info, int request_id, uint64_t session_id) = 0;
    virtual void PyOnOrderEvent(const nb::dict &order_info, const nb::dict &error_info, uint64_t session_id) = 0;
    virtual void PyOnTradeEvent(const nb::dict &trade_info, uint64_t session_id) = 0;
    virtual void PyOnCancelOrderError(const nb::dict &cancel_info, const nb::dict &error_info, uint64_t session_id) = 0;
    virtual void PyOnQueryOrder(const nb::dict &order_info, const nb::dict &error_info, int request_id, bool is_last, uint64_t session_id) = 0;
    virtual void PyOnQueryOrderEx(const nb::dict &order_info, const nb::dict &error_info, int request_id, bool is_last, uint64_t session_id) = 0;
    virtual void PyOnQueryOrderByPage(const nb::dict &order_info, int64_t req_count, int64_t order_sequence, int64_t query_reference, int request_id, bool is_last, uint64_t session_id) = 0;
    virtual void PyOnQueryOrderByPageEx(const nb::dict &order_info, int64_t req_count, int64_t order_sequence, int64_t query_reference, int request_id, bool is_last, uint64_t session_id) = 0;
    virtual void PyOnQueryTrade(const nb::dict &trade_info, const nb::dict &error_info, int request_id, bool is_last, uint64_t session_id) = 0;
    virtual void PyOnQueryTradeByPage(const nb::dict &trade_info, int64_t req_count, int64_t trade_sequence, int64_t query_reference, int request_id, bool is_last, uint64_t session_id) = 0;
    virtual void PyOnQueryPosition(const nb::dict &position, const nb::dict &error_info, int request_id, bool is_last, uint64_t session_id) = 0;
    virtual void PyOnQueryAsset(const nb::dict &asset, const nb::dict &error_info, int request_id, bool is_last, uint64_t session_id) = 0;
    virtual void PyOnQueryStructuredFund(const nb::dict &fund_info, const nb::dict &error_info, int request_id, bool is_last, uint64_t session_id) = 0;
    virtual void PyOnQueryFundTransfer(const nb::dict &fund_transfer_info, const nb::dict &error_info, int request_id, bool is_last, uint64_t session_id) = 0;
    virtual void PyOnFundTransfer(const nb::dict &fund_transfer_info, const nb::dict &error_info, uint64_t session_id) = 0;
    virtual void PyOnQueryOtherServerFund(const nb::dict &fund_info, const nb::dict &error_info, int request_id, uint64_t session_id) = 0;
    virtual void PyOnQueryETF(const nb::dict &etf_info, const nb::dict &error_info, int request_id, bool is_last, uint64_t session_id) = 0;
    virtual void PyOnQueryETFBasket(const nb::dict &etf_component_info, const nb::dict &error_info, int request_id, bool is_last, uint64_t session_id) = 0;
    virtual void PyOnQueryIPOInfoList(const nb::dict &ipo_info, const nb::dict &error_info, int request_id, bool is_last, uint64_t session_id) = 0;
    virtual void PyOnQueryIPOQuotaInfo(const nb::dict &quota_info, const nb::dict &error_info, int request_id, bool is_last, uint64_t session_id) = 0;
    virtual void PyOnQueryOptionAuctionInfo(const nb::dict &option_info, const nb::dict &error_info, int request_id, bool is_last, uint64_t session_id) = 0;
    virtual void PyOnCreditCashRepay(const nb::dict &cash_repay_info, const nb::dict &error_info, uint64_t session_id) = 0;
    virtual void PyOnCreditCashRepayDebtInterestFee(const nb::dict &cash_repay_info, const nb::dict &error_info, uint64_t session_id) = 0;
    virtual void PyOnQueryCreditCashRepayInfo(const nb::dict &cash_repay_info, const nb::dict &error_info, int request_id, bool is_last, uint64_t session_id) = 0;
    virtual void PyOnQueryCreditFundInfo(const nb::dict &fund_info, const nb::dict &error_info, int request_id, uint64_t session_id) = 0;
    virtual void PyOnQueryCreditDebtInfo(const nb::dict &debt_info, const nb::dict &error_info, int request_id, bool is_last, uint64_t session_id) = 0;
    virtual void PyOnQueryCreditTickerDebtInfo(const nb::dict &debt_info, const nb::dict &error_info, int request_id, bool is_last, uint64_t session_id) = 0;
    virtual void PyOnQueryCreditAssetDebtInfo(double remain_amount, const nb::dict &error_info, int request_id, uint64_t session_id) = 0;
    virtual void PyOnQueryCreditTickerAssignInfo(const nb::dict &assign_info, const nb::dict &error_info, int request_id, bool is_last, uint64_t session_id) = 0;
    virtual void PyOnQueryCreditExcessStock(const nb::dict &stock_info, const nb::dict &error_info, int request_id, uint64_t session_id) = 0;
    virtual void PyOnQueryMulCreditExcessStock(const nb::dict &stock_info, const nb::dict &error_info, int request_id, uint64_t session_id, bool is_last) = 0;
    virtual void PyOnCreditExtendDebtDate(const nb::dict &debt_extend_info, const nb::dict &error_info, uint64_t session_id) = 0;
    virtual void PyOnQueryCreditExtendDebtDateOrders(const nb::dict &debt_extend_info, const nb::dict &error_info, int request_id, bool is_last, uint64_t session_id) = 0;
    virtual void PyOnQueryCreditFundExtraInfo(const nb::dict &fund_info, const nb::dict &error_info, int request_id, uint64_t session_id) = 0;
    virtual void PyOnQueryCreditPositionExtraInfo(const nb::dict &fund_info, const nb::dict &error_info, int request_id, bool is_last, uint64_t session_id) = 0;
    virtual void PyOnOptionCombinedOrderEvent(const nb::dict &order_info, const nb::dict &error_info, uint64_t session_id) = 0;
    virtual void PyOnOptionCombinedTradeEvent(const nb::dict &trade_info, uint64_t session_id) = 0;
    virtual void PyOnCancelOptionCombinedOrderError(const nb::dict &cancel_info, const nb::dict &error_info, uint64_t session_id) = 0;
    virtual void PyOnQueryOptionCombinedOrders(const nb::dict &order_info, const nb::dict &error_info, int request_id, bool is_last, uint64_t session_id) = 0;
    virtual void PyOnQueryOptionCombinedOrdersEx(const nb::dict &order_info, const nb::dict &error_info, int request_id, bool is_last, uint64_t session_id) = 0;
    virtual void PyOnQueryOptionCombinedOrdersByPage(const nb::dict &order_info, int64_t req_count, int64_t order_sequence, int64_t query_reference, int request_id, bool is_last, uint64_t session_id) = 0;
    virtual void PyOnQueryOptionCombinedOrdersByPageEx(const nb::dict &order_info, int64_t req_count, int64_t order_sequence, int64_t query_reference, int request_id, bool is_last, uint64_t session_id) = 0;
    virtual void PyOnQueryOptionCombinedTrades(const nb::dict &trade_info, const nb::dict &error_info, int request_id, bool is_last, uint64_t session_id) = 0;
    virtual void PyOnQueryOptionCombinedTradesByPage(const nb::dict &trade_info, int64_t req_count, int64_t trade_sequence, int64_t query_reference, int request_id, bool is_last, uint64_t session_id) = 0;
    virtual void PyOnQueryOptionCombinedPosition(const nb::dict &position_info, const nb::dict &error_info, int request_id, bool is_last, uint64_t session_id) = 0;
    virtual void PyOnQueryOptionCombinedStrategyInfo(const nb::dict &strategy_info, const nb::dict &error_info, int request_id, bool is_last, uint64_t session_id) = 0;
    virtual void PyOnQueryOptionCombinedExecPosition(const nb::dict &position_info, const nb::dict &error_info, int request_id, bool is_last, uint64_t session_id) = 0;
    virtual void PyOnQueryStrategy(const nb::dict &strategy_info, const char* strategy_param, const nb::dict &error_info, int32_t request_id, bool is_last, uint64_t session_id) = 0;
    virtual void PyOnStrategyStateReport(const nb::dict &strategy_state, uint64_t session_id) = 0;
    virtual void PyOnALGOUserEstablishChannel(const char* user, const nb::dict &error_info, uint64_t session_id) = 0;
    virtual void PyOnInsertAlgoOrder(const nb::dict &strategy_info, const nb::dict &error_info, uint64_t session_id) = 0;
    virtual void PyOnCancelAlgoOrder(const nb::dict &strategy_info, const nb::dict &error_info, uint64_t session_id) = 0;
    virtual void PyOnAlgoDisconnected(int reason) = 0;
    virtual void PyOnAlgoConnected() = 0;
    virtual void PyOnStrategySymbolStateReport(const nb::dict &strategy_symbol_state, uint64_t session_id) = 0;
    virtual void PyOnNewStrategyCreateReport(const nb::dict &strategy_info, const char* strategy_param, uint64_t session_id) = 0;
    virtual void PyOnStrategyRecommendation(bool basket_flag, const nb::dict &recommendation_info, const char* strategy_param,const nb::dict &error_info, int32_t request_id, bool is_last, uint64_t session_id) = 0;
};


class PyTdApi final : public TdApi {
public:
    NB_TRAMPOLINE(TdApi, 59);

    void PyOnDisconnected(uint64_t session_id, int reason) override {
        NB_OVERRIDE_PURE_NAME(
                "OnDisconnected",
                PyOnDisconnected,
                session_id,
                reason
        );
    }

    void PyOnError(const nb::dict &error_info) override {
        NB_OVERRIDE_PURE_NAME(
                "OnError",
                PyOnError,
                error_info
        );
    }

    void PyOnQueryAccountTradeMarket(int trade_location, const nb::dict &error_info, int request_id, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnQueryAccountTradeMarket",
                PyOnQueryAccountTradeMarket,
                trade_location,
                error_info,
                request_id,
                session_id
        );
    }

    void PyOnOrderEvent(const nb::dict &order_info, const nb::dict &error_info, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnOrderEvent",
                PyOnOrderEvent,
                order_info,
                error_info,
                session_id
        );
    }
    void PyOnTradeEvent(const nb::dict &trade_info, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnTradeEvent",
                PyOnTradeEvent,
                trade_info,
                session_id
        );
    }

    void PyOnCancelOrderError(const nb::dict &cancel_info, const nb::dict &error_info, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnCancelOrderError",
                PyOnCancelOrderError,
                cancel_info,
                error_info,
                session_id
        );
    }

    void PyOnQueryOrder(const nb::dict &order_info, const nb::dict &error_info, int request_id, bool is_last, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnQueryOrder",
                PyOnQueryOrder,
                order_info,
                error_info,
                request_id,
                is_last,
                session_id
        );
    }

    void PyOnQueryOrderEx(const nb::dict &order_info, const nb::dict &error_info, int request_id, bool is_last, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnQueryOrderEx",
                PyOnQueryOrderEx,
                order_info,
                error_info,
                request_id,
                is_last,
                session_id
        );
    }

    void PyOnQueryOrderByPage(const nb::dict &order_info, int64_t req_count, int64_t order_sequence, int64_t query_reference, int request_id, bool is_last, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnQueryOrderByPage",
                PyOnQueryOrderByPage,
                order_info,
                req_count,
                order_sequence,
                query_reference,
                request_id,
                is_last,
                session_id
        );
    }

    void PyOnQueryOrderByPageEx(const nb::dict &order_info, int64_t req_count, int64_t order_sequence, int64_t query_reference, int request_id, bool is_last, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnQueryOrderByPageEx",
                PyOnQueryOrderByPageEx,
                order_info,
                req_count,
                order_sequence,
                query_reference,
                request_id,
                is_last,
                session_id
        );
    }

    void PyOnQueryTrade(const nb::dict &trade_info, const nb::dict &error_info, int request_id, bool is_last, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnQueryTrade",
                PyOnQueryTrade,
                trade_info,
                error_info,
                request_id,
                is_last,
                session_id
        );
    }

    void PyOnQueryTradeByPage(const nb::dict &trade_info, int64_t req_count, int64_t trade_sequence, int64_t query_reference, int request_id, bool is_last, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnQueryTradeByPage",
                PyOnQueryTradeByPage,
                trade_info,
                req_count,
                trade_sequence,
                query_reference,
                request_id,
                is_last,
                session_id
        );
    }

    void PyOnQueryPosition(const nb::dict &position, const nb::dict &error_info, int request_id, bool is_last, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnQueryPosition",
                PyOnQueryPosition,
                position,
                error_info,
                request_id,
                is_last,
                session_id
        );
    }

    void PyOnQueryAsset(const nb::dict &asset, const nb::dict &error_info, int request_id, bool is_last, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnQueryAsset",
                PyOnQueryAsset,
                asset,
                error_info,
                request_id,
                is_last,
                session_id
        );
    }

    void PyOnQueryStructuredFund(const nb::dict &fund_info, const nb::dict &error_info, int request_id, bool is_last, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnQueryStructuredFund",
                PyOnQueryStructuredFund,
                fund_info,
                error_info,
                request_id,
                is_last,
                session_id
        );
    }

    void PyOnQueryFundTransfer(const nb::dict &fund_transfer_info, const nb::dict &error_info, int request_id, bool is_last, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnQueryFundTransfer",
                PyOnQueryFundTransfer,
                fund_transfer_info,
                error_info,
                request_id,
                is_last,
                session_id
        );
    }

    void PyOnFundTransfer(const nb::dict &fund_transfer_info, const nb::dict &error_info, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnFundTransfer",
                PyOnFundTransfer,
                fund_transfer_info,
                error_info,
                session_id
        );
    }

    void PyOnQueryOtherServerFund(const nb::dict &fund_info, const nb::dict &error_info, int request_id, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnQueryOtherServerFund",
                PyOnQueryOtherServerFund,
                fund_info,
                error_info,
                request_id,
                session_id
        );
    }

    void PyOnQueryETF(const nb::dict &etf_info, const nb::dict &error_info, int request_id, bool is_last, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnQueryETF",
                PyOnQueryETF,
                etf_info,
                error_info,
                request_id,
                is_last,
                session_id
        );
    }

    void PyOnQueryETFBasket(const nb::dict &etf_component_info, const nb::dict &error_info, int request_id, bool is_last, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnQueryETFBasket",
                PyOnQueryETFBasket,
                etf_component_info,
                error_info,
                request_id,
                is_last,
                session_id
        );
    }

    void PyOnQueryIPOInfoList(const nb::dict &ipo_info, const nb::dict &error_info, int request_id, bool is_last, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnQueryIPOInfoList",
                PyOnQueryIPOInfoList,
                ipo_info,
                error_info,
                request_id,
                is_last,
                session_id
        );
    }

    void PyOnQueryIPOQuotaInfo(const nb::dict &quota_info, const nb::dict &error_info, int request_id, bool is_last, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnQueryIPOQuotaInfo",
                PyOnQueryIPOQuotaInfo,
                quota_info,
                error_info,
                request_id,
                is_last,
                session_id
        );
    }

    void PyOnQueryOptionAuctionInfo(const nb::dict &option_info, const nb::dict &error_info, int request_id, bool is_last, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnQueryOptionAuctionInfo",
                PyOnQueryOptionAuctionInfo,
                option_info,
                error_info,
                request_id,
                is_last,
                session_id
        );
    }

    void PyOnCreditCashRepay(const nb::dict &cash_repay_info, const nb::dict &error_info, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnCreditCashRepay",
                PyOnCreditCashRepay,
                cash_repay_info,
                error_info,
                session_id
        );
    }

    void PyOnCreditCashRepayDebtInterestFee(const nb::dict &cash_repay_info, const nb::dict &error_info, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnCreditCashRepayDebtInterestFee",
                PyOnCreditCashRepayDebtInterestFee,
                cash_repay_info,
                error_info,
                session_id
        );
    }

    void PyOnQueryCreditCashRepayInfo(const nb::dict &cash_repay_info, const nb::dict &error_info, int request_id, bool is_last, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnQueryCreditCashRepayInfo",
                PyOnQueryCreditCashRepayInfo,
                cash_repay_info,
                error_info,
                request_id,
                is_last,
                session_id
        );
    }

    void PyOnQueryCreditFundInfo(const nb::dict &fund_info, const nb::dict &error_info, int request_id, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnQueryCreditFundInfo",
                PyOnQueryCreditFundInfo,
                fund_info,
                error_info,
                request_id,
                session_id
        );
    }

    void PyOnQueryCreditDebtInfo(const nb::dict &debt_info, const nb::dict &error_info, int request_id, bool is_last, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnQueryCreditDebtInfo",
                PyOnQueryCreditDebtInfo,
                debt_info,
                error_info,
                request_id,
                is_last,
                session_id
        );
    }

    void PyOnQueryCreditTickerDebtInfo(const nb::dict &debt_info, const nb::dict &error_info, int request_id, bool is_last, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnQueryCreditTickerDebtInfo",
                PyOnQueryCreditTickerDebtInfo,
                debt_info,
                error_info,
                request_id,
                is_last,
                session_id
        );
    }

    void PyOnQueryCreditAssetDebtInfo(double remain_amount, const nb::dict &error_info, int request_id, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnQueryCreditAssetDebtInfo",
                PyOnQueryCreditAssetDebtInfo,
                remain_amount,
                error_info,
                request_id,
                session_id
        );
    }

    void PyOnQueryCreditTickerAssignInfo(const nb::dict &assign_info, const nb::dict &error_info, int request_id, bool is_last, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnQueryCreditTickerAssignInfo",
                PyOnQueryCreditTickerAssignInfo,
                assign_info,
                error_info,
                request_id,
                is_last,
                session_id
        );
    }

    void PyOnQueryCreditExcessStock(const nb::dict &stock_info, const nb::dict &error_info, int request_id, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnQueryCreditExcessStock",
                PyOnQueryCreditExcessStock,
                stock_info,
                error_info,
                request_id,
                session_id
        );
    }

    void PyOnQueryMulCreditExcessStock(const nb::dict &stock_info, const nb::dict &error_info, int request_id, uint64_t session_id, bool is_last) override {
        NB_OVERRIDE_PURE_NAME(
                "OnQueryMulCreditExcessStock",
                PyOnQueryMulCreditExcessStock,
                stock_info,
                error_info,
                request_id,
                session_id,
                is_last
        );
    }

    void PyOnCreditExtendDebtDate(const nb::dict &debt_extend_info, const nb::dict &error_info, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnCreditExtendDebtDate",
                PyOnCreditExtendDebtDate,
                debt_extend_info,
                error_info,
                session_id
        );
    }

    void PyOnQueryCreditExtendDebtDateOrders(const nb::dict &debt_extend_info, const nb::dict &error_info, int request_id, bool is_last, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnQueryCreditExtendDebtDateOrders",
                PyOnQueryCreditExtendDebtDateOrders,
                debt_extend_info,
                error_info,
                request_id,
                is_last,
                session_id
        );
    }

    void PyOnQueryCreditFundExtraInfo(const nb::dict &fund_info, const nb::dict &error_info, int request_id, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnQueryCreditFundExtraInfo",
                PyOnQueryCreditFundExtraInfo,
                fund_info,
                error_info,
                request_id,
                session_id
        );
    }

    void PyOnQueryCreditPositionExtraInfo(const nb::dict &fund_info, const nb::dict &error_info, int request_id, bool is_last, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnQueryCreditPositionExtraInfo",
                PyOnQueryCreditPositionExtraInfo,
                fund_info,
                error_info,
                request_id,
                is_last,
                session_id
        );
    }

    void PyOnOptionCombinedOrderEvent(const nb::dict &order_info, const nb::dict &error_info, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnOptionCombinedOrderEvent",
                PyOnOptionCombinedOrderEvent,
                order_info,
                error_info,
                session_id
        );
    }

    void PyOnOptionCombinedTradeEvent(const nb::dict &trade_info, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnOptionCombinedTradeEvent",
                PyOnOptionCombinedTradeEvent,
                trade_info,
                session_id
        );
    }

    void PyOnCancelOptionCombinedOrderError(const nb::dict &cancel_info, const nb::dict &error_info, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnCancelOptionCombinedOrderError",
                PyOnCancelOptionCombinedOrderError,
                cancel_info,
                error_info,
                session_id
        );
    }

    void PyOnQueryOptionCombinedOrders(const nb::dict &order_info, const nb::dict &error_info, int request_id, bool is_last, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnQueryOptionCombinedOrders",
                PyOnQueryOptionCombinedOrders,
                order_info,
                error_info,
                request_id,
                is_last,
                session_id
        );
    }

    void PyOnQueryOptionCombinedOrdersEx(const nb::dict &order_info, const nb::dict &error_info, int request_id, bool is_last, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnQueryOptionCombinedOrdersEx",
                PyOnQueryOptionCombinedOrdersEx,
                order_info,
                error_info,
                request_id,
                is_last,
                session_id
        );
    }

    void PyOnQueryOptionCombinedOrdersByPage(const nb::dict &order_info, int64_t req_count, int64_t order_sequence, int64_t query_reference, int request_id, bool is_last, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnQueryOptionCombinedOrdersByPage",
                PyOnQueryOptionCombinedOrdersByPage,
                order_info,
                req_count,
                order_sequence,
                query_reference,
                request_id,
                is_last,
                session_id
        );
    }

    void PyOnQueryOptionCombinedOrdersByPageEx(const nb::dict &order_info, int64_t req_count, int64_t order_sequence, int64_t query_reference, int request_id, bool is_last, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnQueryOptionCombinedOrdersByPageEx",
                PyOnQueryOptionCombinedOrdersByPageEx,
                order_info,
                req_count,
                order_sequence,
                query_reference,
                request_id,
                is_last,
                session_id
        );
    }

    void PyOnQueryOptionCombinedTrades(const nb::dict &trade_info, const nb::dict &error_info, int request_id, bool is_last, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnQueryOptionCombinedTrades",
                PyOnQueryOptionCombinedTrades,
                trade_info,
                error_info,
                request_id,
                is_last,
                session_id
        );
    }

    void PyOnQueryOptionCombinedTradesByPage(const nb::dict &trade_info, int64_t req_count, int64_t trade_sequence, int64_t query_reference, int request_id, bool is_last, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnQueryOptionCombinedTradesByPage",
                PyOnQueryOptionCombinedTradesByPage,
                trade_info,
                req_count,
                trade_sequence,
                query_reference,
                request_id,
                is_last,
                session_id
        );
    }

    void PyOnQueryOptionCombinedPosition(const nb::dict &position_info, const nb::dict &error_info, int request_id, bool is_last, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnQueryOptionCombinedPosition",
                PyOnQueryOptionCombinedPosition,
                position_info,
                error_info,
                request_id,
                is_last,
                session_id
        );
    }

    void PyOnQueryOptionCombinedStrategyInfo(const nb::dict &strategy_info, const nb::dict &error_info, int request_id, bool is_last, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnQueryOptionCombinedStrategyInfo",
                PyOnQueryOptionCombinedStrategyInfo,
                strategy_info,
                error_info,
                request_id,
                is_last,
                session_id
        );
    }

    void PyOnQueryOptionCombinedExecPosition(const nb::dict &position_info, const nb::dict &error_info, int request_id, bool is_last, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnQueryOptionCombinedExecPosition",
                PyOnQueryOptionCombinedExecPosition,
                position_info,
                error_info,
                request_id,
                is_last,
                session_id
        );
    }

    void PyOnQueryStrategy(const nb::dict &strategy_info, const char* strategy_param, const nb::dict &error_info, int32_t request_id, bool is_last, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnQueryStrategy",
                PyOnQueryStrategy,
                strategy_info,
                strategy_param,
                error_info,
                request_id,
                is_last,
                session_id
        );
    }

    void PyOnStrategyStateReport(const nb::dict &strategy_state, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnStrategyStateReport",
                PyOnStrategyStateReport,
                strategy_state,
                session_id
        );
    }

    void PyOnALGOUserEstablishChannel(const char* user, const nb::dict &error_info, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnALGOUserEstablishChannel",
                PyOnALGOUserEstablishChannel,
                user,
                error_info,
                session_id
        );
    }

    void PyOnInsertAlgoOrder(const nb::dict &strategy_info, const nb::dict &error_info, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnInsertAlgoOrder",
                PyOnInsertAlgoOrder,
                strategy_info,
                error_info,
                session_id
        );
    }

    void PyOnCancelAlgoOrder(const nb::dict &strategy_info, const nb::dict &error_info, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnCancelAlgoOrder",
                PyOnCancelAlgoOrder,
                strategy_info,
                error_info,
                session_id
        );
    }

    void PyOnAlgoDisconnected(int reason) override {
        NB_OVERRIDE_PURE_NAME(
                "OnAlgoDisconnected",
                PyOnAlgoDisconnected,
                reason
        );
    }

    void PyOnAlgoConnected() override {
        NB_OVERRIDE_PURE_NAME(
                "OnAlgoConnected",
                PyOnAlgoConnected
        );
    }

    void PyOnStrategySymbolStateReport(const nb::dict &strategy_symbol_state, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnStrategySymbolStateReport",
                PyOnStrategySymbolStateReport,
                strategy_symbol_state,
                session_id
        );
    }

    void PyOnNewStrategyCreateReport(const nb::dict &strategy_info, const char* strategy_param, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnNewStrategyCreateReport",
                PyOnNewStrategyCreateReport,
                strategy_info,
                strategy_param,
                session_id
        );
    }

    void PyOnStrategyRecommendation(bool basket_flag, const nb::dict &recommendation_info, const char* strategy_param,const nb::dict &error_info, int32_t request_id, bool is_last, uint64_t session_id) override {
        NB_OVERRIDE_PURE_NAME(
                "OnStrategyRecommendation",
                PyOnStrategyRecommendation,
                basket_flag,
                recommendation_info,
                strategy_param,
                error_info,
                request_id,
                is_last,
                session_id
        );
    }
};

#endif //TD_API_H
