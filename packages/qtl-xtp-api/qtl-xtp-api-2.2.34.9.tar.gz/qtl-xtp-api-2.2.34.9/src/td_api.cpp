#include "td_api.h"


void TdApi::CreateTraderApi(int client_id, const std::string &save_file_path, int log_level) {
    queue_ = std::make_unique<DispatchQueue>();
    api_ = xtp::TraderApi::CreateTraderApi(client_id, save_file_path.c_str(), XTP_LOG_LEVEL(log_level));
    api_->RegisterSpi(this);
}

void TdApi::Destroy() {
    api_->RegisterSpi(nullptr);
    api_->Release();
    api_ = nullptr;
    queue_ = nullptr;
}

std::string TdApi::GetTradingDay() {
    return api_->GetTradingDay();
}

std::string TdApi::GetApiVersion() {
    return api_->GetApiVersion();
}

nb::dict TdApi::GetApiLastError() {
    auto *error_ = api_->GetApiLastError();
    nb::dict error{};
    error["error_id"] = error_->error_id;
    error["error_msg"] = error_->error_msg;
    return error;
}

uint8_t TdApi::GetClientIDByXTPID(uint64_t order_xtp_id) {
    return api_->GetClientIDByXTPID(order_xtp_id);
}

std::string TdApi::GetAccountByXTPID(uint64_t order_xtp_id) {
    return api_->GetAccountByXTPID(order_xtp_id);
}

void TdApi::SubscribePublicTopic(XTP_TE_RESUME_TYPE resume_type) {
    api_->SubscribePublicTopic(resume_type);
}

void TdApi::SetSoftwareVersion(const char *version) {
    api_->SetSoftwareVersion(version);
}

void TdApi::SetSoftwareKey(const char *key) {
    api_->SetSoftwareKey(key);
}

void TdApi::SetHeartBeatInterval(uint32_t interval) {
    api_->SetHeartBeatInterval(interval);
}

uint64_t TdApi::Login(const char *ip, int port, const char *user, const char *password, XTP_PROTOCOL_TYPE sock_type,
                      const char *local_ip) {
    return api_->Login(ip, port, user, password, sock_type, local_ip);
}

int TdApi::Logout(uint64_t session_id) {
    return api_->Logout(session_id);
}

bool TdApi::IsServerRestart(uint64_t session_id) {
    return api_->IsServerRestart(session_id);
}

int TdApi::ModifyUserTerminalInfo(const nb::dict &info, uint64_t session_id) {
    XTPUserTerminalInfoReq req{};
    set_str_field(req.local_ip, info, "local_ip", sizeof(req.local_ip));
    set_str_field(req.mac_addr, info, "mac_addr", sizeof(req.mac_addr));
    set_str_field(req.hd, info, "hd", sizeof(req.hd));
    set_num_field<XTPTerminalType>(req.term_type, info, "term_type");
    set_str_field(req.internet_ip, info, "internet_ip", sizeof(req.internet_ip));
    set_num_field<int32_t>(req.internet_port, info, "internet_port");
    set_str_field(req.client_version, info, "client_version", sizeof(req.client_version));
    set_str_field(req.macos_sno, info, "macos_sno", sizeof(req.macos_sno));
    set_str_field(req.unused, info, "unused", sizeof(req.unused));
    return api_->ModifyUserTerminalInfo(&req, session_id);
}

int TdApi::QueryAccountTradeMarket(uint64_t session_id, int request_id) {
    return api_->QueryAccountTradeMarket(session_id, request_id);
}

uint64_t TdApi::GetANewOrderXTPID(uint64_t session_id) {
    return api_->GetANewOrderXTPID(session_id);
}

uint64_t TdApi::InsertOrder(const nb::dict &order, uint64_t session_id) {
    XTPOrderInsertInfo order_{};
    set_num_field<uint64_t>(order_.order_xtp_id, order, "order_xtp_id");
    set_num_field<uint32_t>(order_.order_client_id, order, "order_client_id");
    set_str_field(order_.ticker, order, "ticker", sizeof(order_.ticker));
    set_num_field<XTP_MARKET_TYPE>(order_.market, order, "market");
    set_num_field<double>(order_.price, order, "price");
    set_num_field<double>(order_.stop_price, order, "stop_price");
    set_num_field<int64_t>(order_.quantity, order, "quantity");
    set_num_field<XTP_PRICE_TYPE>(order_.price_type, order, "price_type");
    set_num_field<XTP_SIDE_TYPE>(order_.side, order, "side");
    set_num_field<XTP_POSITION_EFFECT_TYPE>(order_.position_effect, order, "position_effect");
    set_num_field<uint8_t>(order_.reserved1, order, "reserved1");
    set_num_field<uint8_t>(order_.reserved2, order, "reserved2");
    set_num_field<XTP_BUSINESS_TYPE>(order_.business_type, order, "business_type");
    return api_->InsertOrder(&order_, session_id);
}

uint64_t TdApi::InsertOrderExtra(const nb::dict &order, uint64_t session_id) {
    XTPOrderInsertInfo order_{};
    set_num_field<uint64_t>(order_.order_xtp_id, order, "order_xtp_id");
    set_num_field<uint32_t>(order_.order_client_id, order, "order_client_id");
    set_str_field(order_.ticker, order, "ticker", sizeof(order_.ticker));
    set_num_field<XTP_MARKET_TYPE>(order_.market, order, "market");
    set_num_field<double>(order_.price, order, "price");
    set_num_field<double>(order_.stop_price, order, "stop_price");
    set_num_field<int64_t>(order_.quantity, order, "quantity");
    set_num_field<XTP_PRICE_TYPE>(order_.price_type, order, "price_type");
    set_num_field<XTP_SIDE_TYPE>(order_.side, order, "side");
    set_num_field<XTP_POSITION_EFFECT_TYPE>(order_.position_effect, order, "position_effect");
    set_num_field<uint8_t>(order_.reserved1, order, "reserved1");
    set_num_field<uint8_t>(order_.reserved2, order, "reserved2");
    set_num_field<XTP_BUSINESS_TYPE>(order_.business_type, order, "business_type");
    return api_->InsertOrderExtra(&order_, session_id);
}

uint64_t TdApi::CancelOrder(const uint64_t order_xtp_id, uint64_t session_id) {
    return api_->CancelOrder(order_xtp_id, session_id);
}

int TdApi::QueryOrderByXTPID(const uint64_t order_xtp_id, uint64_t session_id, int request_id) {
    return api_->QueryOrderByXTPID(order_xtp_id, session_id, request_id);
}

int TdApi::QueryOrders(const nb::dict &query_param, uint64_t session_id, int request_id) {
    XTPQueryOrderReq req{};
    set_str_field(req.ticker, query_param, "ticker", sizeof(req.ticker));
    set_num_field<int64_t>(req.begin_time, query_param, "begin_time");
    set_num_field<int64_t>(req.end_time, query_param, "end_time");
    return api_->QueryOrders(&req, session_id, request_id);
}

int TdApi::QueryUnfinishedOrders(uint64_t session_id, int request_id) {
    return api_->QueryUnfinishedOrders(session_id, request_id);
}

int TdApi::QueryOrdersByPage(const nb::dict &query_param, uint64_t session_id, int request_id) {
    XTPQueryOrderByPageReq req{};
    set_num_field<int64_t>(req.req_count, query_param, "req_count");
    set_num_field<int64_t>(req.reference, query_param, "reference");
    set_num_field<int64_t>(req.reserved, query_param, "reserved");
    return api_->QueryOrdersByPage(&req, session_id, request_id);
}

int TdApi::QueryOrderByXTPIDEx(const uint64_t order_xtp_id, uint64_t session_id, int request_id) {
    return api_->QueryOrderByXTPIDEx(order_xtp_id, session_id, request_id);
}

int TdApi::QueryOrdersEx(const nb::dict &query_param, uint64_t session_id, int request_id) {
    XTPQueryOrderReq req{};
    set_str_field(req.ticker, query_param, "ticker", sizeof(req.ticker));
    set_num_field<int64_t>(req.begin_time, query_param, "begin_time");
    set_num_field<int64_t>(req.end_time, query_param, "end_time");
    return api_->QueryOrdersEx(&req, session_id, request_id);
}

int TdApi::QueryUnfinishedOrdersEx(uint64_t session_id, int request_id) {
    return api_->QueryUnfinishedOrdersEx(session_id, request_id);
}

int TdApi::QueryOrdersByPageEx(const nb::dict &query_param, uint64_t session_id, int request_id) {
    XTPQueryOrderByPageReq req{};
    set_num_field<int64_t>(req.req_count, query_param, "req_count");
    set_num_field<int64_t>(req.reference, query_param, "reference");
    set_num_field<int64_t>(req.reserved, query_param, "reserved");
    return api_->QueryOrdersByPageEx(&req, session_id, request_id);
}

int TdApi::QueryTradesByXTPID(const uint64_t order_xtp_id, uint64_t session_id, int request_id) {
    return api_->QueryTradesByXTPID(order_xtp_id, session_id, request_id);
}

int TdApi::QueryTrades(const nb::dict &query_param, uint64_t session_id, int request_id) {
    XTPQueryTraderReq req{};
    set_str_field(req.ticker, query_param, "ticker", sizeof(req.ticker));
    set_num_field<int64_t>(req.begin_time, query_param, "begin_time");
    set_num_field<int64_t>(req.end_time, query_param, "end_time");
    return api_->QueryTrades(&req, session_id, request_id);
}

int TdApi::QueryTradesByPage(const nb::dict &query_param, uint64_t session_id, int request_id) {
    XTPQueryTraderByPageReq req{};
    set_num_field<int64_t>(req.req_count, query_param, "req_count");
    set_num_field<int64_t>(req.reference, query_param, "reference");
    set_num_field<int64_t>(req.reserved, query_param, "reserved");
    return api_->QueryTradesByPage(&req, session_id, request_id);
}

int TdApi::QueryPosition(const char *ticker, uint64_t session_id, int request_id, XTP_MARKET_TYPE market) {
    return api_->QueryPosition(ticker, session_id, request_id, market);
}

int TdApi::QueryAsset(uint64_t session_id, int request_id) {
    return api_->QueryAsset(session_id, request_id);
}

int TdApi::QueryStructuredFund(const nb::dict &query_param, uint64_t session_id, int request_id) {
    XTPQueryStructuredFundInfoReq req{};
    set_num_field<XTP_EXCHANGE_TYPE>(req.exchange_id, query_param, "exchange_id");
    set_str_field(req.sf_ticker, query_param, "sf_ticker", sizeof(req.sf_ticker));
    return api_->QueryStructuredFund(&req, session_id, request_id);
}

uint64_t TdApi::FundTransfer(const nb::dict &fund_transfer, uint64_t session_id) {
    XTPFundTransferReq req{};
    set_num_field<uint64_t>(req.serial_id, fund_transfer, "serial_id");
    set_str_field(req.fund_account, fund_transfer, "fund_account", sizeof(req.fund_account));
    set_str_field(req.password, fund_transfer, "password", sizeof(req.password));
    set_num_field<double>(req.amount, fund_transfer, "amount");
    set_num_field<XTP_FUND_TRANSFER_TYPE>(req.transfer_type, fund_transfer, "transfer_type");
    return api_->FundTransfer(&req, session_id);
}

int TdApi::QueryFundTransfer(const nb::dict &query_param, uint64_t session_id, int request_id) {
    XTPQueryFundTransferLogReq req{};
    set_num_field<uint64_t>(req.serial_id, query_param, "serial_id");
    return api_->QueryFundTransfer(&req, session_id, request_id);
}

int TdApi::QueryOtherServerFund(const nb::dict &query_param, uint64_t session_id, int request_id) {
    XTPFundQueryReq req{};
    set_str_field(req.fund_account, query_param, "fund_account", sizeof(req.fund_account));
    set_str_field(req.password, query_param, "password", sizeof(req.password));
    set_num_field<XTP_FUND_QUERY_TYPE>(req.query_type, query_param, "query_type");
    return 0;
}

int TdApi::QueryETF(const nb::dict &query_param, uint64_t session_id, int request_id) {
    XTPQueryETFBaseReq req{};
    set_num_field<XTP_MARKET_TYPE>(req.market, query_param, "market");
    set_str_field(req.ticker, query_param, "ticker", sizeof(req.ticker));
    return api_->QueryETF(&req, session_id, request_id);
}

int TdApi::QueryETFTickerBasket(const nb::dict &query_param, uint64_t session_id, int request_id) {
    XTPQueryETFComponentReq req{};
    set_num_field<XTP_MARKET_TYPE>(req.market, query_param, "market");
    set_str_field(req.ticker, query_param, "ticker", sizeof(req.ticker));
    return api_->QueryETFTickerBasket(&req, session_id, request_id);
}

int TdApi::QueryIPOInfoList(uint64_t session_id, int request_id) {
    return api_->QueryIPOInfoList(session_id, request_id);
}

int TdApi::QueryIPOQuotaInfo(uint64_t session_id, int request_id) {
    return api_->QueryIPOQuotaInfo(session_id, request_id);
}

int TdApi::QueryOptionAuctionInfo(const nb::dict &query_param, uint64_t session_id, int request_id) {
    XTPQueryOptionAuctionInfoReq req{};
    set_num_field<XTP_MARKET_TYPE>(req.market, query_param, "market");
    set_str_field(req.ticker, query_param, "ticker", sizeof(req.ticker));
    return api_->QueryOptionAuctionInfo(&req, session_id, request_id);
}

uint64_t TdApi::CreditCashRepay(double amount, uint64_t session_id) {
    return api_->CreditCashRepay(amount, session_id);
}

uint64_t TdApi::CreditCashRepayDebtInterestFee(const char *debt_id, double amount, uint64_t session_id) {
    return api_->CreditCashRepayDebtInterestFee(debt_id, amount, session_id);
}

uint64_t TdApi::CreditSellStockRepayDebtInterestFee(const nb::dict &order, const char *debt_id, uint64_t session_id) {
    XTPOrderInsertInfo order_{};
    set_num_field<uint64_t>(order_.order_xtp_id, order, "order_xtp_id");
    set_num_field<uint32_t>(order_.order_client_id, order, "order_client_id");
    set_str_field(order_.ticker, order, "ticker", sizeof(order_.ticker));
    set_num_field<XTP_MARKET_TYPE>(order_.market, order, "market");
    set_num_field<double>(order_.price, order, "price");
    set_num_field<double>(order_.stop_price, order, "stop_price");
    set_num_field<int64_t>(order_.quantity, order, "quantity");
    set_num_field<XTP_PRICE_TYPE>(order_.price_type, order, "price_type");
    set_num_field<XTP_SIDE_TYPE>(order_.side, order, "side");
    set_num_field<XTP_POSITION_EFFECT_TYPE>(order_.position_effect, order, "position_effect");
    set_num_field<uint8_t>(order_.reserved1, order, "reserved1");
    set_num_field<uint8_t>(order_.reserved2, order, "reserved2");
    set_num_field<XTP_BUSINESS_TYPE>(order_.business_type, order, "business_type");
    return api_->CreditSellStockRepayDebtInterestFee(&order_, debt_id, session_id);
}

int TdApi::QueryCreditCashRepayInfo(uint64_t session_id, int request_id) {
    return api_->QueryCreditCashRepayInfo(session_id, request_id);
}

int TdApi::QueryCreditFundInfo(uint64_t session_id, int request_id) {
    return api_->QueryCreditFundInfo(session_id, request_id);
}

int TdApi::QueryCreditDebtInfo(uint64_t session_id, int request_id) {
    return api_->QueryCreditDebtInfo(session_id, request_id);
}

int TdApi::QueryCreditTickerDebtInfo(const nb::dict &query_param, uint64_t session_id, int request_id) {
    XTPClientQueryCrdDebtStockReq req{};
    set_num_field<XTP_MARKET_TYPE>(req.market, query_param, "market");
    set_str_field(req.ticker, query_param, "ticker", sizeof(req.ticker));
    return api_->QueryCreditTickerDebtInfo(&req, session_id, request_id);
}

int TdApi::QueryCreditAssetDebtInfo(uint64_t session_id, int request_id) {
    return api_->QueryCreditAssetDebtInfo(session_id, request_id);
}

int TdApi::QueryCreditTickerAssignInfo(const nb::dict &query_param, uint64_t session_id, int request_id) {
    XTPClientQueryCrdPositionStockReq req{};
    set_num_field<XTP_MARKET_TYPE>(req.market, query_param, "market");
    set_str_field(req.ticker, query_param, "ticker", sizeof(req.ticker));
    return api_->QueryCreditTickerAssignInfo(&req, session_id, request_id);
}

int TdApi::QueryCreditExcessStock(const nb::dict &query_param, uint64_t session_id, int request_id) {
    XTPClientQueryCrdSurplusStkReqInfo req{};
    set_num_field<XTP_MARKET_TYPE>(req.market, query_param, "market");
    set_str_field(req.ticker, query_param, "ticker", sizeof(req.ticker));
    return api_->QueryCreditExcessStock(&req, session_id, request_id);
}

int TdApi::QueryMulCreditExcessStock(const nb::dict &query_param, uint64_t session_id, int request_id) {
    XTPClientQueryCrdSurplusStkReqInfo req{};
    set_num_field<XTP_MARKET_TYPE>(req.market, query_param, "market");
    set_str_field(req.ticker, query_param, "ticker", sizeof(req.ticker));
    return api_->QueryMulCreditExcessStock(&req, session_id, request_id);
}

uint64_t TdApi::CreditExtendDebtDate(const nb::dict &debt_extend, uint64_t session_id) {
    XTPCreditDebtExtendReq req{};
    set_num_field<uint64_t>(req.xtpid, debt_extend, "xtpid");
    set_str_field(req.debt_id, debt_extend, "debt_id", sizeof(req.debt_id));
    set_num_field<uint32_t>(req.defer_days, debt_extend, "defer_days");
    set_str_field(req.fund_account, debt_extend, "fund_account", sizeof(req.fund_account));
    set_str_field(req.password, debt_extend, "password", sizeof(req.password));
    return api_->CreditExtendDebtDate(&req, session_id);
}

int TdApi::QueryCreditExtendDebtDateOrders(uint64_t xtp_id, uint64_t session_id, int request_id) {
    return api_->QueryCreditExtendDebtDateOrders(xtp_id, session_id, request_id);
}

int TdApi::QueryCreditFundExtraInfo(uint64_t session_id, int request_id) {
    return api_->QueryCreditFundExtraInfo(session_id, request_id);
}

int TdApi::QueryCreditPositionExtraInfo(const nb::dict &query_param, uint64_t session_id, int request_id) {
    XTPClientQueryCrdPositionStockReq req{};
    set_num_field<XTP_MARKET_TYPE>(req.market, query_param, "market");
    set_str_field(req.ticker, query_param, "ticker", sizeof(req.ticker));
    return api_->QueryCreditPositionExtraInfo(&req, session_id, request_id);
}

uint64_t TdApi::InsertOptionCombinedOrder(const nb::dict &order, uint64_t session_id) {
    XTPOptCombOrderInsertInfo req{};
    set_num_field<uint64_t>(req.order_xtp_id, order, "order_xtp_id");
    set_num_field<uint32_t>(req.order_client_id, order, "order_client_id");
    set_num_field<XTP_MARKET_TYPE>(req.market, order, "market");
    set_num_field<int64_t>(req.quantity, order, "quantity");
    set_num_field<XTP_SIDE_TYPE>(req.side, order, "side");
    set_num_field<XTP_BUSINESS_TYPE>(req.business_type, order, "business_type");

    strncpy(req.opt_comb_info.strategy_id, nb::cast<std::string>(order["opt_comb_info"]["strategy_id"]).c_str(), sizeof(req.opt_comb_info.strategy_id));
    strncpy(req.opt_comb_info.comb_num, nb::cast<std::string>(order["opt_comb_info"]["comb_num"]).c_str(), sizeof(req.opt_comb_info.comb_num));
    req.opt_comb_info.num_legs = nb::cast<int32_t>(order["opt_comb_info"]["num_legs"]);
    for (int i = 0; i< req.opt_comb_info.num_legs; i++)
    {
        strncpy(req.opt_comb_info.leg_detail[i].leg_security_id, nb::cast<std::string>(order["opt_comb_info"]["leg_detail"][i]["leg_security_id"]).c_str(), sizeof(req.opt_comb_info.leg_detail[i].leg_security_id));
        req.opt_comb_info.leg_detail[i].leg_cntr_type = nb::cast<XTP_OPT_CALL_OR_PUT_TYPE>(order["opt_comb_info"]["leg_detail"][i]["leg_cntr_type"]);
        req.opt_comb_info.leg_detail[i].leg_side = nb::cast<XTP_POSITION_DIRECTION_TYPE>(order["opt_comb_info"]["leg_detail"][i]["leg_side"]);
        req.opt_comb_info.leg_detail[i].leg_covered = nb::cast<XTP_OPT_COVERED_OR_UNCOVERED>(order["opt_comb_info"]["leg_detail"][i]["leg_covered"]);
        req.opt_comb_info.leg_detail[i].leg_qty = nb::cast<int32_t>(order["opt_comb_info"]["leg_detail"][i]["leg_qty"]);
    }
    return api_->InsertOptionCombinedOrder(&req, session_id);
}

uint64_t TdApi::InsertOptionCombinedOrderExtra(const nb::dict &order, uint64_t session_id) {
    XTPOptCombOrderInsertInfo req{};
    set_num_field<uint64_t>(req.order_xtp_id, order, "order_xtp_id");
    set_num_field<uint32_t>(req.order_client_id, order, "order_client_id");
    set_num_field<XTP_MARKET_TYPE>(req.market, order, "market");
    set_num_field<int64_t>(req.quantity, order, "quantity");
    set_num_field<XTP_SIDE_TYPE>(req.side, order, "side");
    set_num_field<XTP_BUSINESS_TYPE>(req.business_type, order, "business_type");

    strncpy(req.opt_comb_info.strategy_id, nb::cast<std::string>(order["opt_comb_info"]["strategy_id"]).c_str(), sizeof(req.opt_comb_info.strategy_id));
    strncpy(req.opt_comb_info.comb_num, nb::cast<std::string>(order["opt_comb_info"]["comb_num"]).c_str(), sizeof(req.opt_comb_info.comb_num));
    req.opt_comb_info.num_legs = nb::cast<int32_t>(order["opt_comb_info"]["num_legs"]);
    for (int i = 0; i< req.opt_comb_info.num_legs; i++)
    {
        strncpy(req.opt_comb_info.leg_detail[i].leg_security_id, nb::cast<std::string>(order["opt_comb_info"]["leg_detail"][i]["leg_security_id"]).c_str(), sizeof(req.opt_comb_info.leg_detail[i].leg_security_id));
        req.opt_comb_info.leg_detail[i].leg_cntr_type = nb::cast<XTP_OPT_CALL_OR_PUT_TYPE>(order["opt_comb_info"]["leg_detail"][i]["leg_cntr_type"]);
        req.opt_comb_info.leg_detail[i].leg_side = nb::cast<XTP_POSITION_DIRECTION_TYPE>(order["opt_comb_info"]["leg_detail"][i]["leg_side"]);
        req.opt_comb_info.leg_detail[i].leg_covered = nb::cast<XTP_OPT_COVERED_OR_UNCOVERED>(order["opt_comb_info"]["leg_detail"][i]["leg_covered"]);
        req.opt_comb_info.leg_detail[i].leg_qty = nb::cast<int32_t>(order["opt_comb_info"]["leg_detail"][i]["leg_qty"]);
    }
    return api_->InsertOptionCombinedOrderExtra(&req, session_id);
}

uint64_t TdApi::CancelOptionCombinedOrder(const uint64_t order_xtp_id, uint64_t session_id) {
    return api_->CancelOptionCombinedOrder(order_xtp_id, session_id);
}

int TdApi::QueryOptionCombinedUnfinishedOrders(uint64_t session_id, int request_id) {
    return api_->QueryOptionCombinedUnfinishedOrders(session_id, request_id);
}

int TdApi::QueryOptionCombinedOrderByXTPID(const uint64_t order_xtp_id, uint64_t session_id, int request_id) {
    return api_->QueryOptionCombinedOrderByXTPID(order_xtp_id, session_id, request_id);
}

int TdApi::QueryOptionCombinedOrders(const nb::dict &query_param, uint64_t session_id, int request_id) {
    XTPQueryOptCombOrderReq req{};
    set_str_field(req.comb_num, query_param, "comb_num", sizeof(req.comb_num));
    set_num_field<int64_t>(req.begin_time, query_param, "begin_time");
    set_num_field<int64_t>(req.end_time, query_param, "end_time");
    return api_->QueryOptionCombinedOrders(&req, session_id, request_id);
}

int TdApi::QueryOptionCombinedOrdersByPage(const nb::dict &query_param, uint64_t session_id, int request_id) {
    XTPQueryOptCombOrderByPageReq req{};
    set_num_field<int64_t>(req.req_count, query_param, "req_count");
    set_num_field<int64_t>(req.reference, query_param, "reference");
    set_num_field<int64_t>(req.reserved, query_param, "reserved");
    return api_->QueryOptionCombinedOrdersByPage(&req, session_id, request_id);
}

int TdApi::QueryOptionCombinedUnfinishedOrdersEx(uint64_t session_id, int request_id) {
    return api_->QueryOptionCombinedUnfinishedOrdersEx(session_id, request_id);
}

int TdApi::QueryOptionCombinedOrderByXTPIDEx(const uint64_t order_xtp_id, uint64_t session_id, int request_id) {
    return api_->QueryOptionCombinedOrderByXTPIDEx(order_xtp_id, session_id, request_id);
}

int TdApi::QueryOptionCombinedOrdersEx(const nb::dict &query_param, uint64_t session_id, int request_id) {
    XTPQueryOptCombOrderReq req{};
    set_str_field(req.comb_num, query_param, "comb_num", sizeof(req.comb_num));
    set_num_field<int64_t>(req.begin_time, query_param, "begin_time");
    set_num_field<int64_t>(req.end_time, query_param, "end_time");
    return api_->QueryOptionCombinedOrdersEx(&req, session_id, request_id);
}

int TdApi::QueryOptionCombinedOrdersByPageEx(const nb::dict &query_param, uint64_t session_id, int request_id) {
    XTPQueryOptCombOrderByPageReq req{};
    set_num_field<int64_t>(req.req_count, query_param, "req_count");
    set_num_field<int64_t>(req.reference, query_param, "reference");
    set_num_field<int64_t>(req.reserved, query_param, "reserved");
    return api_->QueryOptionCombinedOrdersByPageEx(&req, session_id, request_id);
}

int TdApi::QueryOptionCombinedTradesByXTPID(const uint64_t order_xtp_id, uint64_t session_id, int request_id) {
    return api_->QueryOptionCombinedTradesByXTPID(order_xtp_id, session_id, request_id);
}

int TdApi::QueryOptionCombinedTrades(const nb::dict &query_param, uint64_t session_id, int request_id) {
    XTPQueryOptCombTraderReq req{};
    set_str_field(req.comb_num, query_param, "comb_num", sizeof(req.comb_num));
    set_num_field<int64_t>(req.begin_time, query_param, "begin_time");
    set_num_field<int64_t>(req.end_time, query_param, "end_time");
    return api_->QueryOptionCombinedTrades(&req, session_id, request_id);
}

int TdApi::QueryOptionCombinedTradesByPage(const nb::dict &query_param, uint64_t session_id, int request_id) {
    XTPQueryOptCombTraderByPageReq req{};
    set_num_field<int64_t>(req.req_count, query_param, "req_count");
    set_num_field<int64_t>(req.reference, query_param, "reference");
    set_num_field<int64_t>(req.reserved, query_param, "reserved");
    return api_->QueryOptionCombinedTradesByPage(&req, session_id, request_id);
}

int TdApi::QueryOptionCombinedPosition(const nb::dict &query_param, uint64_t session_id, int request_id) {
    XTPQueryOptCombPositionReq req{};
    set_str_field(req.comb_num, query_param, "comb_num", sizeof(req.comb_num));
    set_num_field<XTP_MARKET_TYPE>(req.market, query_param, "market");
    return api_->QueryOptionCombinedPosition(&req, session_id, request_id);
}

int TdApi::QueryOptionCombinedStrategyInfo(uint64_t session_id, int request_id) {
    return api_->QueryOptionCombinedStrategyInfo(session_id, request_id);
}

int TdApi::QueryOptionCombinedExecPosition(const nb::dict &query_param, uint64_t session_id, int request_id) {
    XTPQueryOptCombExecPosReq req{};
    set_num_field<XTP_MARKET_TYPE>(req.market, query_param, "market");
    set_str_field(req.cntrt_code_1, query_param, "cntrt_code_1", sizeof(req.cntrt_code_1));
    set_str_field(req.cntrt_code_2, query_param, "cntrt_code_2", sizeof(req.cntrt_code_2));
    return api_->QueryOptionCombinedExecPosition(&req, session_id, request_id);
}

int TdApi::LoginALGO(const char *ip, int port, const char *user, const char *password, XTP_PROTOCOL_TYPE sock_type,
                     const char *local_ip) {
    return api_->LoginALGO(ip, port, user, password, sock_type, local_ip);
}

int
TdApi::QueryStrategy(uint32_t strategy_type, uint64_t client_strategy_id, uint64_t xtp_strategy_id, uint64_t session_id,
                     int32_t request_id) {
    return api_->QueryStrategy(strategy_type, client_strategy_id, xtp_strategy_id, session_id, request_id);
}

int TdApi::ALGOUserEstablishChannel(const char *oms_ip, int oms_port, const char *user, const char *password,
                                    uint64_t session_id) {
    return api_->ALGOUserEstablishChannel(oms_ip, oms_port, user, password, session_id);
}

int
TdApi::InsertAlgoOrder(uint32_t strategy_type, uint64_t client_strategy_id, const char *strategy_param, uint64_t session_id) {
    return api_->InsertAlgoOrder(strategy_type, client_strategy_id, const_cast<char *>(strategy_param), session_id);
}

int TdApi::CancelAlgoOrder(bool cancel_flag, uint64_t xtp_strategy_id, uint64_t session_id) {
    return api_->CancelAlgoOrder(cancel_flag, xtp_strategy_id, session_id);
}

uint64_t TdApi::GetAlgorithmIDByOrder(uint64_t order_xtp_id, uint32_t order_client_id) {
    return api_->GetAlgorithmIDByOrder(order_xtp_id, order_client_id);
}

int TdApi::StrategyRecommendation(bool basket_flag, const char *basket_param, uint64_t session_id, int32_t request_id) {
    return api_->StrategyRecommendation(basket_flag, const_cast<char *>(basket_param), session_id, request_id);
}

void TdApi::OnDisconnected(uint64_t session_id, int reason) {
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        PyOnDisconnected(session_id, reason);
    });
}

void TdApi::OnError(XTPRI *error_info) {
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnError(py_error);
    });
}

void TdApi::OnQueryAccountTradeMarket(int trade_location, XTPRI *error_info, int request_id, uint64_t session_id) {
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnQueryAccountTradeMarket(trade_location, py_error, request_id, session_id);
    });
}

void TdApi::OnOrderEvent(XTPOrderInfo *order_info, XTPRI *error_info, uint64_t session_id) {
    bool has_data{false};
    XTPOrderInfo order_info_{};
    if (order_info) {
        has_data = true;
        order_info_ = *order_info;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_order_info{};
        if (has_data) {
            py_order_info["order_xtp_id"] = order_info_.order_xtp_id;
            py_order_info["order_client_id"] = order_info_.order_client_id;
            py_order_info["order_cancel_client_id"] = order_info_.order_cancel_client_id;
            py_order_info["order_cancel_xtp_id"] = order_info_.order_cancel_xtp_id;
            py_order_info["ticker"] = order_info_.ticker;
            py_order_info["market"] = order_info_.market;
            py_order_info["price"] = order_info_.price;
            py_order_info["quantity"] = order_info_.quantity;
            py_order_info["price_type"] = order_info_.price_type;
            py_order_info["side"] = order_info_.side;
            py_order_info["position_effect"] = order_info_.position_effect;
            py_order_info["business_type"] = order_info_.business_type;
            py_order_info["qty_traded"] = order_info_.qty_traded;
            py_order_info["qty_left"] = order_info_.qty_left;
            py_order_info["insert_time"] = order_info_.insert_time;
            py_order_info["update_time"] = order_info_.update_time;
            py_order_info["cancel_time"] = order_info_.cancel_time;
            py_order_info["trade_amount"] = order_info_.trade_amount;
            py_order_info["order_local_id"] = order_info_.order_local_id;
            py_order_info["order_status"] = order_info_.order_status;
            py_order_info["order_submit_status"] = order_info_.order_submit_status;
            py_order_info["order_type"] = order_info_.order_type;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnOrderEvent(py_order_info, py_error, session_id);
    });
}

void TdApi::OnTradeEvent(XTPTradeReport *trade_info, uint64_t session_id) {
    bool has_data{false};
    XTPTradeReport trade_info_{};
    if (trade_info) {
        has_data = true;
        trade_info_ = *trade_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_trade_info{};
        if (has_data) {
            py_trade_info["order_xtp_id"] = trade_info_.order_xtp_id;
            py_trade_info["order_client_id"] = trade_info_.order_client_id;
            py_trade_info["ticker"] = trade_info_.ticker;
            py_trade_info["market"] = trade_info_.market;
            py_trade_info["local_order_id"] = trade_info_.local_order_id;
            py_trade_info["exec_id"] = trade_info_.exec_id;
            py_trade_info["price"] = trade_info_.price;
            py_trade_info["quantity"] = trade_info_.quantity;
            py_trade_info["trade_time"] = trade_info_.trade_time;
            py_trade_info["trade_amount"] = trade_info_.trade_amount;
            py_trade_info["report_index"] = trade_info_.report_index;
            py_trade_info["order_exch_id"] = trade_info_.order_exch_id;
            py_trade_info["trade_type"] = trade_info_.trade_type;
            py_trade_info["side"] = trade_info_.side;
            py_trade_info["position_effect"] = trade_info_.position_effect;
            py_trade_info["business_type"] = trade_info_.business_type;
            py_trade_info["branch_pbu"] = trade_info_.branch_pbu;
        }
        PyOnTradeEvent(py_trade_info, session_id);
    });
}

void TdApi::OnCancelOrderError(XTPOrderCancelInfo *cancel_info, XTPRI *error_info, uint64_t session_id) {
    bool has_data{false};
    XTPOrderCancelInfo cancel_info_{};
    if (cancel_info) {
        has_data = true;
        cancel_info_ = *cancel_info;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_cancel_info{};
        if (has_data) {
            py_cancel_info["order_cancel_xtp_id"] = cancel_info_.order_cancel_xtp_id;
            py_cancel_info["order_xtp_id"] = cancel_info_.order_xtp_id;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnCancelOrderError(py_cancel_info, py_error, session_id);
    });
}

void TdApi::OnQueryOrder(XTPQueryOrderRsp *order_info, XTPRI *error_info, int request_id, bool is_last,
                         uint64_t session_id) {
    bool has_data{false};
    XTPQueryOrderRsp order_info_{};
    if (order_info) {
        has_data = true;
        order_info_ = *order_info;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_order_info{};
        if (has_data) {
            py_order_info["order_xtp_id"] = order_info_.order_xtp_id;
            py_order_info["order_client_id"] = order_info_.order_client_id;
            py_order_info["order_cancel_client_id"] = order_info_.order_cancel_client_id;
            py_order_info["order_cancel_xtp_id"] = order_info_.order_cancel_xtp_id;
            py_order_info["ticker"] = order_info_.ticker;
            py_order_info["market"] = order_info_.market;
            py_order_info["price"] = order_info_.price;
            py_order_info["quantity"] = order_info_.quantity;
            py_order_info["price_type"] = order_info_.price_type;
            py_order_info["side"] = order_info_.side;
            py_order_info["position_effect"] = order_info_.position_effect;
            py_order_info["business_type"] = order_info_.business_type;
            py_order_info["qty_traded"] = order_info_.qty_traded;
            py_order_info["qty_left"] = order_info_.qty_left;
            py_order_info["insert_time"] = order_info_.insert_time;
            py_order_info["update_time"] = order_info_.update_time;
            py_order_info["cancel_time"] = order_info_.cancel_time;
            py_order_info["trade_amount"] = order_info_.trade_amount;
            py_order_info["order_local_id"] = order_info_.order_local_id;
            py_order_info["order_status"] = order_info_.order_status;
            py_order_info["order_submit_status"] = order_info_.order_submit_status;
            py_order_info["order_type"] = order_info_.order_type;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnQueryOrder(py_order_info, py_error, request_id, is_last, session_id);
    });
}

void TdApi::OnQueryOrderEx(XTPOrderInfoEx *order_info, XTPRI *error_info, int request_id, bool is_last,
                           uint64_t session_id) {
    bool has_data{false};
    XTPOrderInfoEx order_info_{};
    if (order_info) {
        has_data = true;
        order_info_ = *order_info;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_order_info{};
        if (has_data) {
            py_order_info["order_xtp_id"] = order_info_.order_xtp_id;
            py_order_info["order_client_id"] = order_info_.order_client_id;
            py_order_info["order_cancel_client_id"] = order_info_.order_cancel_client_id;
            py_order_info["order_cancel_xtp_id"] = order_info_.order_cancel_xtp_id;
            py_order_info["ticker"] = order_info_.ticker;
            py_order_info["market"] = order_info_.market;
            py_order_info["price"] = order_info_.price;
            py_order_info["quantity"] = order_info_.quantity;
            py_order_info["price_type"] = order_info_.price_type;
            py_order_info["side"] = order_info_.side;
            py_order_info["position_effect"] = order_info_.position_effect;
            py_order_info["business_type"] = order_info_.business_type;
            py_order_info["qty_traded"] = order_info_.qty_traded;
            py_order_info["qty_left"] = order_info_.qty_left;
            py_order_info["insert_time"] = order_info_.insert_time;
            py_order_info["update_time"] = order_info_.update_time;
            py_order_info["cancel_time"] = order_info_.cancel_time;
            py_order_info["trade_amount"] = order_info_.trade_amount;
            py_order_info["order_local_id"] = order_info_.order_local_id;
            py_order_info["order_status"] = order_info_.order_status;
            py_order_info["order_submit_status"] = order_info_.order_submit_status;
            py_order_info["order_type"] = order_info_.order_type;
            py_order_info["order_exch_id"] = order_info_.order_exch_id;
            nb::dict order_err_t_{};
            order_err_t_["error_id"] = order_info_.order_err_t.error_id;
            order_err_t_["error_msg"] = order_info_.order_err_t.error_msg;
            py_order_info["order_err_t"] = order_err_t_;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnQueryOrderEx(py_order_info, py_error, request_id, is_last, session_id);
    });
}

void TdApi::OnQueryOrderByPage(XTPQueryOrderRsp *order_info, int64_t req_count, int64_t order_sequence,
                               int64_t query_reference, int request_id, bool is_last, uint64_t session_id) {
    bool has_data{false};
    XTPQueryOrderRsp order_info_{};
    if (order_info) {
        has_data = true;
        order_info_ = *order_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_order_info{};
        if (has_data) {
            py_order_info["order_xtp_id"] = order_info_.order_xtp_id;
            py_order_info["order_client_id"] = order_info_.order_client_id;
            py_order_info["order_cancel_client_id"] = order_info_.order_cancel_client_id;
            py_order_info["order_cancel_xtp_id"] = order_info_.order_cancel_xtp_id;
            py_order_info["ticker"] = order_info_.ticker;
            py_order_info["market"] = order_info_.market;
            py_order_info["price"] = order_info_.price;
            py_order_info["quantity"] = order_info_.quantity;
            py_order_info["price_type"] = order_info_.price_type;
            py_order_info["side"] = order_info_.side;
            py_order_info["position_effect"] = order_info_.position_effect;
            py_order_info["business_type"] = order_info_.business_type;
            py_order_info["qty_traded"] = order_info_.qty_traded;
            py_order_info["qty_left"] = order_info_.qty_left;
            py_order_info["insert_time"] = order_info_.insert_time;
            py_order_info["update_time"] = order_info_.update_time;
            py_order_info["cancel_time"] = order_info_.cancel_time;
            py_order_info["trade_amount"] = order_info_.trade_amount;
            py_order_info["order_local_id"] = order_info_.order_local_id;
            py_order_info["order_status"] = order_info_.order_status;
            py_order_info["order_submit_status"] = order_info_.order_submit_status;
            py_order_info["order_type"] = order_info_.order_type;
        }
        PyOnQueryOrderByPage(py_order_info, req_count, order_sequence, query_reference, request_id, is_last, session_id);
    });
}

void TdApi::OnQueryOrderByPageEx(XTPOrderInfoEx *order_info, int64_t req_count, int64_t order_sequence,
                                 int64_t query_reference, int request_id, bool is_last, uint64_t session_id) {
    bool has_data{false};
    XTPOrderInfoEx order_info_{};
    if (order_info) {
        has_data = true;
        order_info_ = *order_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_order_info{};
        if (has_data) {
            py_order_info["order_xtp_id"] = order_info_.order_xtp_id;
            py_order_info["order_client_id"] = order_info_.order_client_id;
            py_order_info["order_cancel_client_id"] = order_info_.order_cancel_client_id;
            py_order_info["order_cancel_xtp_id"] = order_info_.order_cancel_xtp_id;
            py_order_info["ticker"] = order_info_.ticker;
            py_order_info["market"] = order_info_.market;
            py_order_info["price"] = order_info_.price;
            py_order_info["quantity"] = order_info_.quantity;
            py_order_info["price_type"] = order_info_.price_type;
            py_order_info["side"] = order_info_.side;
            py_order_info["position_effect"] = order_info_.position_effect;
            py_order_info["business_type"] = order_info_.business_type;
            py_order_info["qty_traded"] = order_info_.qty_traded;
            py_order_info["qty_left"] = order_info_.qty_left;
            py_order_info["insert_time"] = order_info_.insert_time;
            py_order_info["update_time"] = order_info_.update_time;
            py_order_info["cancel_time"] = order_info_.cancel_time;
            py_order_info["trade_amount"] = order_info_.trade_amount;
            py_order_info["order_local_id"] = order_info_.order_local_id;
            py_order_info["order_status"] = order_info_.order_status;
            py_order_info["order_submit_status"] = order_info_.order_submit_status;
            py_order_info["order_type"] = order_info_.order_type;
            py_order_info["order_exch_id"] = order_info_.order_exch_id;
            nb::dict order_err_t_{};
            order_err_t_["error_id"] = order_info_.order_err_t.error_id;
            order_err_t_["error_msg"] = order_info_.order_err_t.error_msg;
            py_order_info["order_err_t"] = order_err_t_;
        }
        PyOnQueryOrderByPageEx(py_order_info, req_count, order_sequence, query_reference, request_id, is_last, session_id);
    });
}

void TdApi::OnQueryTrade(XTPQueryTradeRsp *trade_info, XTPRI *error_info, int request_id, bool is_last,
                         uint64_t session_id) {
    bool has_data{false};
    XTPQueryTradeRsp trade_info_{};
    if (trade_info) {
        has_data = true;
        trade_info_ = *trade_info;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_trade_info{};
        if (has_data) {
            py_trade_info["order_xtp_id"] = trade_info_.order_xtp_id;
            py_trade_info["order_client_id"] = trade_info_.order_client_id;
            py_trade_info["ticker"] = trade_info_.ticker;
            py_trade_info["market"] = trade_info_.market;
            py_trade_info["local_order_id"] = trade_info_.local_order_id;
            py_trade_info["exec_id"] = trade_info_.exec_id;
            py_trade_info["price"] = trade_info_.price;
            py_trade_info["quantity"] = trade_info_.quantity;
            py_trade_info["trade_time"] = trade_info_.trade_time;
            py_trade_info["trade_amount"] = trade_info_.trade_amount;
            py_trade_info["report_index"] = trade_info_.report_index;
            py_trade_info["order_exch_id"] = trade_info_.order_exch_id;
            py_trade_info["trade_type"] = trade_info_.trade_type;
            py_trade_info["side"] = trade_info_.side;
            py_trade_info["position_effect"] = trade_info_.position_effect;
            py_trade_info["business_type"] = trade_info_.business_type;
            py_trade_info["branch_pbu"] = trade_info_.branch_pbu;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnTradeEvent(py_trade_info, session_id);
    });
}

void TdApi::OnQueryTradeByPage(XTPQueryTradeRsp *trade_info, int64_t req_count, int64_t trade_sequence,
                               int64_t query_reference, int request_id, bool is_last, uint64_t session_id) {
    bool has_data{false};
    XTPQueryTradeRsp trade_info_{};
    if (trade_info) {
        has_data = true;
        trade_info_ = *trade_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_trade_info{};
        if (has_data) {
            py_trade_info["order_xtp_id"] = trade_info_.order_xtp_id;
            py_trade_info["order_client_id"] = trade_info_.order_client_id;
            py_trade_info["ticker"] = trade_info_.ticker;
            py_trade_info["market"] = trade_info_.market;
            py_trade_info["local_order_id"] = trade_info_.local_order_id;
            py_trade_info["exec_id"] = trade_info_.exec_id;
            py_trade_info["price"] = trade_info_.price;
            py_trade_info["quantity"] = trade_info_.quantity;
            py_trade_info["trade_time"] = trade_info_.trade_time;
            py_trade_info["trade_amount"] = trade_info_.trade_amount;
            py_trade_info["report_index"] = trade_info_.report_index;
            py_trade_info["order_exch_id"] = trade_info_.order_exch_id;
            py_trade_info["trade_type"] = trade_info_.trade_type;
            py_trade_info["side"] = trade_info_.side;
            py_trade_info["position_effect"] = trade_info_.position_effect;
            py_trade_info["business_type"] = trade_info_.business_type;
            py_trade_info["branch_pbu"] = trade_info_.branch_pbu;
        }
        PyOnQueryTradeByPage(py_trade_info, req_count, trade_sequence, query_reference, request_id, is_last, session_id);
    });
}

void TdApi::OnQueryPosition(XTPQueryStkPositionRsp *position, XTPRI *error_info, int request_id, bool is_last,
                            uint64_t session_id) {
    bool has_data{false};
    XTPQueryStkPositionRsp position_{};
    if (position) {
        has_data = true;
        position_ = *position;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_position{};
        if (has_data) {
            py_position["ticker"] = position_.ticker;
            py_position["ticker_name"] = position_.ticker_name;
            py_position["market"] = position_.market;
            py_position["total_qty"] = position_.total_qty;
            py_position["sellable_qty"] = position_.sellable_qty;
            py_position["avg_price"] = position_.avg_price;
            py_position["unrealized_pnl"] = position_.unrealized_pnl;
            py_position["yesterday_position"] = position_.yesterday_position;
            py_position["purchase_redeemable_qty"] = position_.purchase_redeemable_qty;
            py_position["position_direction"] = position_.position_direction;
            py_position["position_security_type"] = position_.position_security_type;
            py_position["executable_option"] = position_.executable_option;
            py_position["lockable_position"] = position_.lockable_position;
            py_position["executable_underlying"] = position_.executable_underlying;
            py_position["locked_position"] = position_.locked_position;
            py_position["usable_locked_position"] = position_.usable_locked_position;
            py_position["profit_price"] = position_.profit_price;
            py_position["buy_cost"] = position_.buy_cost;
            py_position["profit_cost"] = position_.profit_cost;
            py_position["market_value"] = position_.market_value;
            py_position["margin"] = position_.margin;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnQueryPosition(py_position, py_error, request_id, is_last, session_id);
    });
}

void
TdApi::OnQueryAsset(XTPQueryAssetRsp *asset, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) {
    bool has_data{false};
    XTPQueryAssetRsp asset_{};
    if (asset) {
        has_data = true;
        asset_ = *asset;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_asset{};
        if (has_data) {
            py_asset["total_asset"] = asset_.total_asset;
            py_asset["buying_power"] = asset_.buying_power;
            py_asset["security_asset"] = asset_.security_asset;
            py_asset["fund_buy_amount"] = asset_.fund_buy_amount;
            py_asset["fund_buy_fee"] = asset_.fund_buy_fee;
            py_asset["fund_sell_amount"] = asset_.fund_sell_amount;
            py_asset["fund_sell_fee"] = asset_.fund_sell_fee;
            py_asset["withholding_amount"] = asset_.withholding_amount;
            py_asset["account_type"] = asset_.account_type;
            py_asset["frozen_margin"] = asset_.frozen_margin;
            py_asset["frozen_exec_cash"] = asset_.frozen_exec_cash;
            py_asset["frozen_exec_fee"] = asset_.frozen_exec_fee;
            py_asset["pay_later"] = asset_.pay_later;
            py_asset["preadva_pay"] = asset_.preadva_pay;
            py_asset["orig_banlance"] = asset_.orig_banlance;
            py_asset["banlance"] = asset_.banlance;
            py_asset["deposit_withdraw"] = asset_.deposit_withdraw;
            py_asset["trade_netting"] = asset_.trade_netting;
            py_asset["captial_asset"] = asset_.captial_asset;
            py_asset["force_freeze_amount"] = asset_.force_freeze_amount;
            py_asset["preferred_amount"] = asset_.preferred_amount;
            py_asset["repay_stock_aval_banlance"] = asset_.repay_stock_aval_banlance;
            py_asset["fund_order_data_charges"] = asset_.fund_order_data_charges;
            py_asset["fund_cancel_data_charges"] = asset_.fund_cancel_data_charges;
            py_asset["exchange_cur_risk_degree"] = asset_.exchange_cur_risk_degree;
            py_asset["company_cur_risk_degree"] = asset_.company_cur_risk_degree;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnQueryAsset(py_asset, py_error, request_id, is_last, session_id);
    });
}

void TdApi::OnQueryStructuredFund(XTPStructuredFundInfo *fund_info, XTPRI *error_info, int request_id, bool is_last,
                                  uint64_t session_id) {
    bool has_data{false};
    XTPStructuredFundInfo fund_info_{};
    if (fund_info) {
        has_data = true;
        fund_info_ = *fund_info;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_fund_info{};
        if (has_data) {
            py_fund_info["exchange_id"] = fund_info_.exchange_id;
            py_fund_info["sf_ticker"] = fund_info_.sf_ticker;
            py_fund_info["sf_ticker_name"] = fund_info_.sf_ticker_name;
            py_fund_info["ticker"] = fund_info_.ticker;
            py_fund_info["ticker_name"] = fund_info_.ticker_name;
            py_fund_info["split_merge_status"] = fund_info_.split_merge_status;
            py_fund_info["ratio"] = fund_info_.ratio;
            py_fund_info["min_split_qty"] = fund_info_.min_split_qty;
            py_fund_info["min_merge_qty"] = fund_info_.min_merge_qty;
            py_fund_info["net_price"] = fund_info_.net_price;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnQueryStructuredFund(py_fund_info, py_error, request_id, is_last, session_id);
    });
}

void
TdApi::OnQueryFundTransfer(XTPFundTransferNotice *fund_transfer_info, XTPRI *error_info, int request_id, bool is_last,
                           uint64_t session_id) {
    bool has_data{false};
    XTPFundTransferNotice fund_transfer_info_{};
    if (fund_transfer_info) {
        has_data = true;
        fund_transfer_info_ = *fund_transfer_info;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_fund_transfer_info{};
        if (has_data) {
            py_fund_transfer_info["serial_id"] = fund_transfer_info_.serial_id;
            py_fund_transfer_info["transfer_type"] = fund_transfer_info_.transfer_type;
            py_fund_transfer_info["amount"] = fund_transfer_info_.amount;
            py_fund_transfer_info["oper_status"] = fund_transfer_info_.oper_status;
            py_fund_transfer_info["transfer_time"] = fund_transfer_info_.transfer_time;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnQueryFundTransfer(py_fund_transfer_info, py_error, request_id, is_last, session_id);
    });
}

void TdApi::OnFundTransfer(XTPFundTransferNotice *fund_transfer_info, XTPRI *error_info, uint64_t session_id) {
    bool has_data{false};
    XTPFundTransferNotice fund_transfer_info_{};
    if (fund_transfer_info) {
        has_data = true;
        fund_transfer_info_ = *fund_transfer_info;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_fund_transfer_info{};
        if (has_data) {
            py_fund_transfer_info["serial_id"] = fund_transfer_info_.serial_id;
            py_fund_transfer_info["transfer_type"] = fund_transfer_info_.transfer_type;
            py_fund_transfer_info["amount"] = fund_transfer_info_.amount;
            py_fund_transfer_info["oper_status"] = fund_transfer_info_.oper_status;
            py_fund_transfer_info["transfer_time"] = fund_transfer_info_.transfer_time;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnFundTransfer(py_fund_transfer_info, py_error, session_id);
    });
}

void TdApi::OnQueryOtherServerFund(XTPFundQueryRsp *fund_info, XTPRI *error_info, int request_id, uint64_t session_id) {
    bool has_data{false};
    XTPFundQueryRsp fund_info_{};
    if (fund_info) {
        has_data = true;
        fund_info_ = *fund_info;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_fund_info{};
        if (has_data) {
            py_fund_info["amount"] = fund_info_.amount;
            py_fund_info["query_type"] = fund_info_.query_type;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnQueryOtherServerFund(py_fund_info, py_error, request_id, session_id);
    });
}

void
TdApi::OnQueryETF(XTPQueryETFBaseRsp *etf_info, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) {
    bool has_data{false};
    XTPQueryETFBaseRsp etf_info_{};
    if (etf_info) {
        has_data = true;
        etf_info_ = *etf_info;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_etf_info{};
        if (has_data) {
            py_etf_info["market"] = etf_info_.market;
            py_etf_info["etf"] = etf_info_.etf;
            py_etf_info["subscribe_redemption_ticker"] = etf_info_.subscribe_redemption_ticker;
            py_etf_info["unit"] = etf_info_.unit;
            py_etf_info["subscribe_status"] = etf_info_.subscribe_status;
            py_etf_info["redemption_status"] = etf_info_.redemption_status;
            py_etf_info["max_cash_ratio"] = etf_info_.max_cash_ratio;
            py_etf_info["estimate_amount"] = etf_info_.estimate_amount;
            py_etf_info["cash_component"] = etf_info_.cash_component;
            py_etf_info["net_value"] = etf_info_.net_value;
            py_etf_info["total_amount"] = etf_info_.total_amount;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnQueryETF(py_etf_info, py_error, request_id, is_last, session_id);
    });
}

void
TdApi::OnQueryETFBasket(XTPQueryETFComponentRsp *etf_component_info, XTPRI *error_info, int request_id, bool is_last,
                        uint64_t session_id) {
    bool has_data{false};
    XTPQueryETFComponentRsp etf_component_info_{};
    if (etf_component_info) {
        has_data = true;
        etf_component_info_ = *etf_component_info;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_etf_component_info{};
        if (has_data) {
            py_etf_component_info["market"] = etf_component_info_.market;
            py_etf_component_info["ticker"] = etf_component_info_.ticker;
            py_etf_component_info["component_ticker"] = etf_component_info_.component_ticker;
            py_etf_component_info["component_name"] = etf_component_info_.component_name;
            py_etf_component_info["quantity"] = etf_component_info_.quantity;
            py_etf_component_info["component_market"] = etf_component_info_.component_market;
            py_etf_component_info["replace_type"] = etf_component_info_.replace_type;
            py_etf_component_info["premium_ratio"] = etf_component_info_.premium_ratio;
            py_etf_component_info["amount"] = etf_component_info_.amount;
            py_etf_component_info["creation_premium_ratio"] = etf_component_info_.creation_premium_ratio;
            py_etf_component_info["redemption_discount_ratio"] = etf_component_info_.redemption_discount_ratio;
            py_etf_component_info["creation_amount"] = etf_component_info_.creation_amount;
            py_etf_component_info["redemption_amount"] = etf_component_info_.redemption_amount;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnQueryETFBasket(py_etf_component_info, py_error, request_id, is_last, session_id);
    });
}

void TdApi::OnQueryIPOInfoList(XTPQueryIPOTickerRsp *ipo_info, XTPRI *error_info, int request_id, bool is_last,
                               uint64_t session_id) {
    bool has_data{false};
    XTPQueryIPOTickerRsp ipo_info_{};
    if (ipo_info) {
        has_data = true;
        ipo_info_ = *ipo_info;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_ipo_info{};
        if (has_data) {
            py_ipo_info["market"] = ipo_info_.market;
            py_ipo_info["ticker"] = ipo_info_.ticker;
            py_ipo_info["ticker_name"] = ipo_info_.ticker_name;
            py_ipo_info["ticker_type"] = ipo_info_.ticker_type;
            py_ipo_info["price"] = ipo_info_.price;
            py_ipo_info["unit"] = ipo_info_.unit;
            py_ipo_info["qty_upper_limit"] = ipo_info_.qty_upper_limit;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnQueryIPOInfoList(py_ipo_info, py_error, request_id, is_last, session_id);
    });
}

void TdApi::OnQueryIPOQuotaInfo(XTPQueryIPOQuotaRsp *quota_info, XTPRI *error_info, int request_id, bool is_last,
                                uint64_t session_id) {
    bool has_data{false};
    XTPQueryIPOQuotaRsp quota_info_{};
    if (quota_info) {
        has_data = true;
        quota_info_ = *quota_info;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_quota_info{};
        if (has_data) {
            py_quota_info["market"] = quota_info_.market;
            py_quota_info["quantity"] = quota_info_.quantity;
            py_quota_info["tech_quantity"] = quota_info_.tech_quantity;
            py_quota_info["unused"] = quota_info_.unused;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnQueryIPOQuotaInfo(py_quota_info, py_error, request_id, is_last, session_id);
    });
}

void TdApi::OnQueryOptionAuctionInfo(XTPQueryOptionAuctionInfoRsp *option_info, XTPRI *error_info, int request_id,
                                     bool is_last, uint64_t session_id) {
    bool has_data{false};
    XTPQueryOptionAuctionInfoRsp option_info_{};
    if (option_info) {
        has_data = true;
        option_info_ = *option_info;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_option_info{};
        if (has_data) {
            py_option_info["ticker"] = option_info_.ticker;
            py_option_info["security_id_source"] = option_info_.security_id_source;
            py_option_info["symbol"] = option_info_.symbol;
            py_option_info["contract_id"] = option_info_.contract_id;
            py_option_info["underlying_security_id"] = option_info_.underlying_security_id;
            py_option_info["underlying_security_id_source"] = option_info_.underlying_security_id_source;
            py_option_info["list_date"] = option_info_.list_date;
            py_option_info["last_trade_date"] = option_info_.last_trade_date;
            py_option_info["ticker_type"] = option_info_.ticker_type;
            py_option_info["day_trading"] = option_info_.day_trading;
            py_option_info["call_or_put"] = option_info_.call_or_put;
            py_option_info["delivery_day"] = option_info_.delivery_day;
            py_option_info["delivery_month"] = option_info_.delivery_month;
            py_option_info["exercise_type"] = option_info_.exercise_type;
            py_option_info["exercise_begin_date"] = option_info_.exercise_begin_date;
            py_option_info["exercise_end_date"] = option_info_.exercise_end_date;
            py_option_info["exercise_price"] = option_info_.exercise_price;
            py_option_info["qty_unit"] = option_info_.qty_unit;
            py_option_info["contract_unit"] = option_info_.contract_unit;
            py_option_info["contract_position"] = option_info_.contract_position;
            py_option_info["prev_close_price"] = option_info_.prev_close_price;
            py_option_info["prev_clearing_price"] = option_info_.prev_clearing_price;
            py_option_info["lmt_buy_max_qty"] = option_info_.lmt_buy_max_qty;
            py_option_info["lmt_buy_min_qty"] = option_info_.lmt_buy_min_qty;
            py_option_info["lmt_sell_max_qty"] = option_info_.lmt_sell_max_qty;
            py_option_info["lmt_sell_min_qty"] = option_info_.lmt_sell_min_qty;
            py_option_info["mkt_buy_max_qty"] = option_info_.mkt_buy_max_qty;
            py_option_info["mkt_buy_min_qty"] = option_info_.mkt_buy_min_qty;
            py_option_info["mkt_sell_max_qty"] = option_info_.mkt_sell_max_qty;
            py_option_info["mkt_sell_min_qty"] = option_info_.mkt_sell_min_qty;
            py_option_info["price_tick"] = option_info_.price_tick;
            py_option_info["upper_limit_price"] = option_info_.upper_limit_price;
            py_option_info["lower_limit_price"] = option_info_.lower_limit_price;
            py_option_info["sell_margin"] = option_info_.sell_margin;
            py_option_info["margin_ratio_param1"] = option_info_.margin_ratio_param1;
            py_option_info["margin_ratio_param2"] = option_info_.margin_ratio_param2;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnQueryOptionAuctionInfo(py_option_info, py_error, request_id, is_last, session_id);
    });
}

void TdApi::OnCreditCashRepay(XTPCrdCashRepayRsp *cash_repay_info, XTPRI *error_info, uint64_t session_id) {
    bool has_data{false};
    XTPCrdCashRepayRsp cash_repay_info_{};
    if (cash_repay_info) {
        has_data = true;
        cash_repay_info_ = *cash_repay_info;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_cash_repay_info{};
        if (has_data) {
            py_cash_repay_info["xtp_id"] = cash_repay_info_.xtp_id;
            py_cash_repay_info["request_amount"] = cash_repay_info_.request_amount;
            py_cash_repay_info["cash_repay_amount"] = cash_repay_info_.cash_repay_amount;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnCreditCashRepay(py_cash_repay_info, py_error, session_id);
    });
}

void TdApi::OnCreditCashRepayDebtInterestFee(XTPCrdCashRepayDebtInterestFeeRsp *cash_repay_info, XTPRI *error_info,
                                             uint64_t session_id) {
    bool has_data{false};
    XTPCrdCashRepayDebtInterestFeeRsp cash_repay_info_{};
    if (cash_repay_info) {
        has_data = true;
        cash_repay_info_ = *cash_repay_info;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_cash_repay_info{};
        if (has_data) {
            py_cash_repay_info["xtp_id"] = cash_repay_info_.xtp_id;
            py_cash_repay_info["request_amount"] = cash_repay_info_.request_amount;
            py_cash_repay_info["cash_repay_amount"] = cash_repay_info_.cash_repay_amount;
            py_cash_repay_info["debt_compact_id"] = cash_repay_info_.debt_compact_id;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnCreditCashRepayDebtInterestFee(py_cash_repay_info, py_error, session_id);
    });
}

void
TdApi::OnQueryCreditCashRepayInfo(XTPCrdCashRepayInfo *cash_repay_info, XTPRI *error_info, int request_id, bool is_last,
                                  uint64_t session_id) {
    bool has_data{false};
    XTPCrdCashRepayInfo cash_repay_info_{};
    if (cash_repay_info) {
        has_data = true;
        cash_repay_info_ = *cash_repay_info;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_cash_repay_info{};
        if (has_data) {
            py_cash_repay_info["xtp_id"] = cash_repay_info_.xtp_id;
            py_cash_repay_info["status"] = cash_repay_info_.status;
            py_cash_repay_info["request_amount"] = cash_repay_info_.request_amount;
            py_cash_repay_info["cash_repay_amount"] = cash_repay_info_.cash_repay_amount;
            py_cash_repay_info["position_effect"] = cash_repay_info_.position_effect;
            nb::dict error_info_{};
            error_info_["error_id"] = cash_repay_info_.error_info.error_id;
            error_info_["error_msg"] = cash_repay_info_.error_info.error_msg;
            py_cash_repay_info["error_info"] = error_info_;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnQueryCreditCashRepayInfo(py_cash_repay_info, py_error, request_id, is_last, session_id);
    });
}

void TdApi::OnQueryCreditFundInfo(XTPCrdFundInfo *fund_info, XTPRI *error_info, int request_id, uint64_t session_id) {
    bool has_data{false};
    XTPCrdFundInfo fund_info_{};
    if (fund_info) {
        has_data = true;
        fund_info_ = *fund_info;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_fund_info{};
        if (has_data) {
            py_fund_info["maintenance_ratio"] = fund_info_.maintenance_ratio;
            py_fund_info["all_asset"] = fund_info_.all_asset;
            py_fund_info["all_debt"] = fund_info_.all_debt;
            py_fund_info["line_of_credit"] = fund_info_.line_of_credit;
            py_fund_info["guaranty"] = fund_info_.guaranty;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnQueryCreditFundInfo(py_fund_info, py_error, request_id, session_id);
    });
}

void TdApi::OnQueryCreditDebtInfo(XTPCrdDebtInfo *debt_info, XTPRI *error_info, int request_id, bool is_last,
                                  uint64_t session_id) {
    bool has_data{false};
    XTPCrdDebtInfo debt_info_{};
    if (debt_info) {
        has_data = true;
        debt_info_ = *debt_info;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_debt_info{};
        if (has_data) {
            py_debt_info["debt_type"] = debt_info_.debt_type;
            py_debt_info["debt_id"] = debt_info_.debt_id;
            py_debt_info["position_id"] = debt_info_.position_id;
            py_debt_info["order_xtp_id"] = debt_info_.order_xtp_id;
            py_debt_info["debt_status"] = debt_info_.debt_status;
            py_debt_info["market"] = debt_info_.market;
            py_debt_info["ticker"] = debt_info_.ticker;
            py_debt_info["order_date"] = debt_info_.order_date;
            py_debt_info["end_date"] = debt_info_.end_date;
            py_debt_info["orig_end_date"] = debt_info_.orig_end_date;
            py_debt_info["is_extended"] = debt_info_.is_extended;
            py_debt_info["remain_amt"] = debt_info_.remain_amt;
            py_debt_info["remain_qty"] = debt_info_.remain_qty;
            py_debt_info["remain_principal"] = debt_info_.remain_principal;
            py_debt_info["due_right_qty"] = debt_info_.due_right_qty;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnQueryCreditDebtInfo(py_debt_info, py_error, request_id, is_last, session_id);
    });
}

void TdApi::OnQueryCreditTickerDebtInfo(XTPCrdDebtStockInfo *debt_info, XTPRI *error_info, int request_id, bool is_last,
                                        uint64_t session_id) {
    bool has_data{false};
    XTPCrdDebtStockInfo debt_info_{};
    if (debt_info) {
        has_data = true;
        debt_info_ = *debt_info;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_debt_info{};
        if (has_data) {
            py_debt_info["market"] = debt_info_.market;
            py_debt_info["ticker"] = debt_info_.ticker;
            py_debt_info["stock_repay_quantity"] = debt_info_.stock_repay_quantity;
            py_debt_info["stock_total_quantity"] = debt_info_.stock_total_quantity;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnQueryCreditTickerDebtInfo(py_debt_info, py_error, request_id, is_last, session_id);
    });
}

void TdApi::OnQueryCreditAssetDebtInfo(double remain_amount, XTPRI *error_info, int request_id, uint64_t session_id) {
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnQueryCreditAssetDebtInfo(remain_amount, py_error, request_id, session_id);
    });
}

void
TdApi::OnQueryCreditTickerAssignInfo(XTPClientQueryCrdPositionStkInfo *assign_info, XTPRI *error_info, int request_id,
                                     bool is_last, uint64_t session_id) {
    bool has_data{false};
    XTPClientQueryCrdPositionStkInfo assign_info_{};
    if (assign_info) {
        has_data = true;
        assign_info_ = *assign_info;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_assign_info{};
        if (has_data) {
            py_assign_info["market"] = assign_info_.market;
            py_assign_info["ticker"] = assign_info_.ticker;
            py_assign_info["limit_qty"] = assign_info_.limit_qty;
            py_assign_info["yesterday_qty"] = assign_info_.yesterday_qty;
            py_assign_info["left_qty"] = assign_info_.left_qty;
            py_assign_info["frozen_qty"] = assign_info_.frozen_qty;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnQueryCreditTickerAssignInfo(py_assign_info, py_error, request_id, is_last, session_id);
    });
}

void TdApi::OnQueryCreditExcessStock(XTPClientQueryCrdSurplusStkRspInfo *stock_info, XTPRI *error_info, int request_id,
                                     uint64_t session_id) {
    bool has_data{false};
    XTPClientQueryCrdSurplusStkRspInfo stock_info_{};
    if (stock_info) {
        has_data = true;
        stock_info_ = *stock_info;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_stock_info{};
        if (has_data) {
            py_stock_info["market"] = stock_info_.market;
            py_stock_info["ticker"] = stock_info_.ticker;
            py_stock_info["transferable_quantity"] = stock_info_.transferable_quantity;
            py_stock_info["transferred_quantity"] = stock_info_.transferred_quantity;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnQueryCreditExcessStock(py_stock_info, py_error, request_id, session_id);
    });
}

void
TdApi::OnQueryMulCreditExcessStock(XTPClientQueryCrdSurplusStkRspInfo *stock_info, XTPRI *error_info, int request_id,
                                   uint64_t session_id, bool is_last) {
    bool has_data{false};
    XTPClientQueryCrdSurplusStkRspInfo stock_info_{};
    if (stock_info) {
        has_data = true;
        stock_info_ = *stock_info;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_stock_info{};
        if (has_data) {
            py_stock_info["market"] = stock_info_.market;
            py_stock_info["ticker"] = stock_info_.ticker;
            py_stock_info["transferable_quantity"] = stock_info_.transferable_quantity;
            py_stock_info["transferred_quantity"] = stock_info_.transferred_quantity;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnQueryMulCreditExcessStock(py_stock_info, py_error, request_id, session_id, is_last);
    });
}

void
TdApi::OnCreditExtendDebtDate(XTPCreditDebtExtendNotice *debt_extend_info, XTPRI *error_info, uint64_t session_id) {
    bool has_data{false};
    XTPCreditDebtExtendNotice debt_extend_info_{};
    if (debt_extend_info) {
        has_data = true;
        debt_extend_info_ = *debt_extend_info;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_debt_extend_info{};
        if (has_data) {
            py_debt_extend_info["xtpid"] = debt_extend_info_.xtpid;
            py_debt_extend_info["debt_id"] = debt_extend_info_.debt_id;
            py_debt_extend_info["oper_status"] = debt_extend_info_.oper_status;
            py_debt_extend_info["oper_time"] = debt_extend_info_.oper_time;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnCreditExtendDebtDate(py_debt_extend_info, py_error, session_id);
    });
}

void
TdApi::OnQueryCreditExtendDebtDateOrders(XTPCreditDebtExtendNotice *debt_extend_info, XTPRI *error_info, int request_id,
                                         bool is_last, uint64_t session_id) {
    bool has_data{false};
    XTPCreditDebtExtendNotice debt_extend_info_{};
    if (debt_extend_info) {
        has_data = true;
        debt_extend_info_ = *debt_extend_info;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_debt_extend_info{};
        if (has_data) {
            py_debt_extend_info["xtpid"] = debt_extend_info_.xtpid;
            py_debt_extend_info["debt_id"] = debt_extend_info_.debt_id;
            py_debt_extend_info["oper_status"] = debt_extend_info_.oper_status;
            py_debt_extend_info["oper_time"] = debt_extend_info_.oper_time;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnQueryCreditExtendDebtDateOrders(py_debt_extend_info, py_error, request_id, is_last, session_id);
    });
}

void TdApi::OnQueryCreditFundExtraInfo(XTPCrdFundExtraInfo *fund_info, XTPRI *error_info, int request_id,
                                       uint64_t session_id) {
    bool has_data{false};
    XTPCrdFundExtraInfo fund_info_{};
    if (fund_info) {
        has_data = true;
        fund_info_ = *fund_info;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_fund_info{};
        if (has_data) {
            py_fund_info["mf_rs_avl_used"] = fund_info_.mf_rs_avl_used;
            py_fund_info["security_capital"] = fund_info_.security_capital;
            py_fund_info["financing_debts"] = fund_info_.financing_debts;
            py_fund_info["short_sell_debts"] = fund_info_.short_sell_debts;
            py_fund_info["contract_debts_load"] = fund_info_.contract_debts_load;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnQueryCreditFundExtraInfo(py_fund_info, py_error, request_id, session_id);
    });
}

void TdApi::OnQueryCreditPositionExtraInfo(XTPCrdPositionExtraInfo *fund_info, XTPRI *error_info, int request_id,
                                           bool is_last, uint64_t session_id) {
    bool has_data{false};
    XTPCrdPositionExtraInfo fund_info_{};
    if (fund_info) {
        has_data = true;
        fund_info_ = *fund_info;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_fund_info{};
        if (has_data) {
            py_fund_info["market"] = fund_info_.market;
            py_fund_info["ticker"] = fund_info_.ticker;
            py_fund_info["mf_rs_avl_used"] = fund_info_.mf_rs_avl_used;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnQueryCreditPositionExtraInfo(py_fund_info, py_error, request_id, is_last, session_id);
    });
}

void TdApi::OnOptionCombinedOrderEvent(XTPOptCombOrderInfo *order_info, XTPRI *error_info, uint64_t session_id) {
    bool has_data{false};
    XTPOptCombOrderInfo order_info_{};
    if (order_info) {
        has_data = true;
        order_info_ = *order_info;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_order_info{};
        if (has_data) {
            py_order_info["order_xtp_id"] = order_info_.order_xtp_id;
            py_order_info["order_client_id"] = order_info_.order_client_id;
            py_order_info["order_cancel_client_id"] = order_info_.order_cancel_client_id;
            py_order_info["order_cancel_xtp_id"] = order_info_.order_cancel_xtp_id;
            py_order_info["market"] = order_info_.market;
            py_order_info["quantity"] = order_info_.quantity;
            py_order_info["side"] = order_info_.side;
            py_order_info["business_type"] = order_info_.business_type;
            py_order_info["qty_traded"] = order_info_.qty_traded;
            py_order_info["qty_left"] = order_info_.qty_left;
            py_order_info["insert_time"] = order_info_.insert_time;
            py_order_info["update_time"] = order_info_.update_time;
            py_order_info["cancel_time"] = order_info_.cancel_time;
            py_order_info["trade_amount"] = order_info_.trade_amount;
            py_order_info["order_local_id"] = order_info_.order_local_id;
            py_order_info["order_status"] = order_info_.order_status;
            py_order_info["order_submit_status"] = order_info_.order_submit_status;
            py_order_info["order_type"] = order_info_.order_type;

            nb::dict opt_comb_info_{};
            opt_comb_info_["strategy_id"] = order_info_.opt_comb_info.strategy_id;
            opt_comb_info_["comb_num"] = order_info_.opt_comb_info.comb_num;
            opt_comb_info_["num_legs"] = order_info_.opt_comb_info.num_legs;

            nb::list leg_detail_{};
            for (int i = 0; i < order_info_.opt_comb_info.num_legs; i++) {
                nb::dict leg_{};
                leg_["leg_security_id"] = order_info_.opt_comb_info.leg_detail[i].leg_security_id;
                leg_["leg_cntr_type"] = order_info_.opt_comb_info.leg_detail[i].leg_cntr_type;
                leg_["leg_side"] = order_info_.opt_comb_info.leg_detail[i].leg_side;
                leg_["leg_covered"] = order_info_.opt_comb_info.leg_detail[i].leg_covered;
                leg_["leg_qty"] = order_info_.opt_comb_info.leg_detail[i].leg_qty;
                leg_detail_.append(leg_);
            }
            opt_comb_info_["leg_detail"] = leg_detail_;

            py_order_info["opt_comb_info"] = opt_comb_info_;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnOptionCombinedOrderEvent(py_order_info, py_error, session_id);
    });
}

void TdApi::OnOptionCombinedTradeEvent(XTPOptCombTradeReport *trade_info, uint64_t session_id) {
    bool has_data{false};
    XTPOptCombTradeReport trade_info_{};
    if (trade_info) {
        has_data = true;
        trade_info_ = *trade_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_trade_info{};
        if (has_data) {
            py_trade_info["order_xtp_id"] = trade_info_.order_xtp_id;
            py_trade_info["order_client_id"] = trade_info_.order_client_id;
            py_trade_info["market"] = trade_info_.market;
            py_trade_info["local_order_id"] = trade_info_.local_order_id;
            py_trade_info["exec_id"] = trade_info_.exec_id;
            py_trade_info["quantity"] = trade_info_.quantity;
            py_trade_info["trade_time"] = trade_info_.trade_time;
            py_trade_info["trade_amount"] = trade_info_.trade_amount;
            py_trade_info["report_index"] = trade_info_.report_index;
            py_trade_info["order_exch_id"] = trade_info_.order_exch_id;
            py_trade_info["trade_type"] = trade_info_.trade_type;
            py_trade_info["side"] = trade_info_.side;
            py_trade_info["business_type"] = trade_info_.business_type;
            py_trade_info["branch_pbu"] = trade_info_.branch_pbu;

            nb::dict opt_comb_info_{};
            opt_comb_info_["strategy_id"] = trade_info_.opt_comb_info.strategy_id;
            opt_comb_info_["comb_num"] = trade_info_.opt_comb_info.comb_num;
            opt_comb_info_["num_legs"] = trade_info_.opt_comb_info.num_legs;

            nb::list leg_detail_{};
            for (int i = 0; i < trade_info_.opt_comb_info.num_legs; i++) {
                nb::dict leg_{};
                leg_["leg_security_id"] = trade_info_.opt_comb_info.leg_detail[i].leg_security_id;
                leg_["leg_cntr_type"] = trade_info_.opt_comb_info.leg_detail[i].leg_cntr_type;
                leg_["leg_side"] = trade_info_.opt_comb_info.leg_detail[i].leg_side;
                leg_["leg_covered"] = trade_info_.opt_comb_info.leg_detail[i].leg_covered;
                leg_["leg_qty"] = trade_info_.opt_comb_info.leg_detail[i].leg_qty;
                leg_detail_.append(leg_);
            }
            opt_comb_info_["leg_detail"] = leg_detail_;

            py_trade_info["opt_comb_info"] = opt_comb_info_;
        }
        PyOnOptionCombinedTradeEvent(py_trade_info, session_id);
    });
}

void TdApi::OnCancelOptionCombinedOrderError(XTPOptCombOrderCancelInfo *cancel_info, XTPRI *error_info,
                                             uint64_t session_id) {
    bool has_data{false};
    XTPOptCombOrderCancelInfo cancel_info_{};
    if (cancel_info) {
        has_data = true;
        cancel_info_ = *cancel_info;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_cancel_info{};
        if (has_data) {
            py_cancel_info["order_cancel_xtp_id"] = cancel_info_.order_cancel_xtp_id;
            py_cancel_info["order_xtp_id"] = cancel_info_.order_xtp_id;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnCancelOptionCombinedOrderError(py_cancel_info, py_error, session_id);
    });
}

void
TdApi::OnQueryOptionCombinedOrders(XTPQueryOptCombOrderRsp *order_info, XTPRI *error_info, int request_id, bool is_last,
                                   uint64_t session_id) {
    bool has_data{false};
    XTPQueryOptCombOrderRsp order_info_{};
    if (order_info) {
        has_data = true;
        order_info_ = *order_info;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_order_info{};
        if (has_data) {
            py_order_info["order_xtp_id"] = order_info_.order_xtp_id;
            py_order_info["order_client_id"] = order_info_.order_client_id;
            py_order_info["order_cancel_client_id"] = order_info_.order_cancel_client_id;
            py_order_info["order_cancel_xtp_id"] = order_info_.order_cancel_xtp_id;
            py_order_info["market"] = order_info_.market;
            py_order_info["quantity"] = order_info_.quantity;
            py_order_info["side"] = order_info_.side;
            py_order_info["business_type"] = order_info_.business_type;
            py_order_info["qty_traded"] = order_info_.qty_traded;
            py_order_info["qty_left"] = order_info_.qty_left;
            py_order_info["insert_time"] = order_info_.insert_time;
            py_order_info["update_time"] = order_info_.update_time;
            py_order_info["cancel_time"] = order_info_.cancel_time;
            py_order_info["trade_amount"] = order_info_.trade_amount;
            py_order_info["order_local_id"] = order_info_.order_local_id;
            py_order_info["order_status"] = order_info_.order_status;
            py_order_info["order_submit_status"] = order_info_.order_submit_status;
            py_order_info["order_type"] = order_info_.order_type;

            nb::dict opt_comb_info_{};
            opt_comb_info_["strategy_id"] = order_info_.opt_comb_info.strategy_id;
            opt_comb_info_["comb_num"] = order_info_.opt_comb_info.comb_num;
            opt_comb_info_["num_legs"] = order_info_.opt_comb_info.num_legs;

            nb::list leg_detail_{};
            for (int i = 0; i < order_info_.opt_comb_info.num_legs; i++) {
                nb::dict leg_{};
                leg_["leg_security_id"] = order_info_.opt_comb_info.leg_detail[i].leg_security_id;
                leg_["leg_cntr_type"] = order_info_.opt_comb_info.leg_detail[i].leg_cntr_type;
                leg_["leg_side"] = order_info_.opt_comb_info.leg_detail[i].leg_side;
                leg_["leg_covered"] = order_info_.opt_comb_info.leg_detail[i].leg_covered;
                leg_["leg_qty"] = order_info_.opt_comb_info.leg_detail[i].leg_qty;
                leg_detail_.append(leg_);
            }
            opt_comb_info_["leg_detail"] = leg_detail_;

            py_order_info["opt_comb_info"] = opt_comb_info_;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnQueryOptionCombinedOrders(py_order_info, py_error, request_id, is_last, session_id);
    });
}

void
TdApi::OnQueryOptionCombinedOrdersEx(XTPOptCombOrderInfoEx *order_info, XTPRI *error_info, int request_id, bool is_last,
                                     uint64_t session_id) {
    bool has_data{false};
    XTPOptCombOrderInfoEx order_info_{};
    if (order_info) {
        has_data = true;
        order_info_ = *order_info;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_order_info{};
        if (has_data) {
            py_order_info["order_xtp_id"] = order_info_.order_xtp_id;
            py_order_info["order_client_id"] = order_info_.order_client_id;
            py_order_info["order_cancel_client_id"] = order_info_.order_cancel_client_id;
            py_order_info["order_cancel_xtp_id"] = order_info_.order_cancel_xtp_id;
            py_order_info["market"] = order_info_.market;
            py_order_info["quantity"] = order_info_.quantity;
            py_order_info["side"] = order_info_.side;
            py_order_info["business_type"] = order_info_.business_type;
            py_order_info["qty_traded"] = order_info_.qty_traded;
            py_order_info["qty_left"] = order_info_.qty_left;
            py_order_info["insert_time"] = order_info_.insert_time;
            py_order_info["update_time"] = order_info_.update_time;
            py_order_info["cancel_time"] = order_info_.cancel_time;
            py_order_info["trade_amount"] = order_info_.trade_amount;
            py_order_info["order_local_id"] = order_info_.order_local_id;
            py_order_info["order_status"] = order_info_.order_status;
            py_order_info["order_submit_status"] = order_info_.order_submit_status;
            py_order_info["order_type"] = order_info_.order_type;

            nb::dict opt_comb_info_{};
            opt_comb_info_["strategy_id"] = order_info_.opt_comb_info.strategy_id;
            opt_comb_info_["comb_num"] = order_info_.opt_comb_info.comb_num;
            opt_comb_info_["num_legs"] = order_info_.opt_comb_info.num_legs;

            nb::list leg_detail_{};
            for (int i = 0; i < order_info_.opt_comb_info.num_legs; i++) {
                nb::dict leg_{};
                leg_["leg_security_id"] = order_info_.opt_comb_info.leg_detail[i].leg_security_id;
                leg_["leg_cntr_type"] = order_info_.opt_comb_info.leg_detail[i].leg_cntr_type;
                leg_["leg_side"] = order_info_.opt_comb_info.leg_detail[i].leg_side;
                leg_["leg_covered"] = order_info_.opt_comb_info.leg_detail[i].leg_covered;
                leg_["leg_qty"] = order_info_.opt_comb_info.leg_detail[i].leg_qty;
                leg_detail_.append(leg_);
            }
            opt_comb_info_["leg_detail"] = leg_detail_;
            py_order_info["opt_comb_info"] = opt_comb_info_;

            py_order_info["order_exch_id"] = order_info_.order_exch_id;

            nb::dict order_err_t_{};
            order_err_t_["error_id"] = order_info_.order_err_t.error_id;
            order_err_t_["error_msg"] = order_info_.order_err_t.error_msg;
            py_order_info["order_err_t"] = order_err_t_;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnQueryOptionCombinedOrdersEx(py_order_info, py_error, request_id, is_last, session_id);
    });
}

void
TdApi::OnQueryOptionCombinedOrdersByPage(XTPQueryOptCombOrderRsp *order_info, int64_t req_count, int64_t order_sequence,
                                         int64_t query_reference, int request_id, bool is_last, uint64_t session_id) {
    bool has_data{false};
    XTPQueryOptCombOrderRsp order_info_{};
    if (order_info) {
        has_data = true;
        order_info_ = *order_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_order_info{};
        if (has_data) {
            py_order_info["order_xtp_id"] = order_info_.order_xtp_id;
            py_order_info["order_client_id"] = order_info_.order_client_id;
            py_order_info["order_cancel_client_id"] = order_info_.order_cancel_client_id;
            py_order_info["order_cancel_xtp_id"] = order_info_.order_cancel_xtp_id;
            py_order_info["market"] = order_info_.market;
            py_order_info["quantity"] = order_info_.quantity;
            py_order_info["side"] = order_info_.side;
            py_order_info["business_type"] = order_info_.business_type;
            py_order_info["qty_traded"] = order_info_.qty_traded;
            py_order_info["qty_left"] = order_info_.qty_left;
            py_order_info["insert_time"] = order_info_.insert_time;
            py_order_info["update_time"] = order_info_.update_time;
            py_order_info["cancel_time"] = order_info_.cancel_time;
            py_order_info["trade_amount"] = order_info_.trade_amount;
            py_order_info["order_local_id"] = order_info_.order_local_id;
            py_order_info["order_status"] = order_info_.order_status;
            py_order_info["order_submit_status"] = order_info_.order_submit_status;
            py_order_info["order_type"] = order_info_.order_type;

            nb::dict opt_comb_info_{};
            opt_comb_info_["strategy_id"] = order_info_.opt_comb_info.strategy_id;
            opt_comb_info_["comb_num"] = order_info_.opt_comb_info.comb_num;
            opt_comb_info_["num_legs"] = order_info_.opt_comb_info.num_legs;

            nb::list leg_detail_{};
            for (int i = 0; i < order_info_.opt_comb_info.num_legs; i++) {
                nb::dict leg_{};
                leg_["leg_security_id"] = order_info_.opt_comb_info.leg_detail[i].leg_security_id;
                leg_["leg_cntr_type"] = order_info_.opt_comb_info.leg_detail[i].leg_cntr_type;
                leg_["leg_side"] = order_info_.opt_comb_info.leg_detail[i].leg_side;
                leg_["leg_covered"] = order_info_.opt_comb_info.leg_detail[i].leg_covered;
                leg_["leg_qty"] = order_info_.opt_comb_info.leg_detail[i].leg_qty;
                leg_detail_.append(leg_);
            }
            opt_comb_info_["leg_detail"] = leg_detail_;

            py_order_info["opt_comb_info"] = opt_comb_info_;
        }
        PyOnQueryOptionCombinedOrdersByPage(py_order_info, req_count, order_sequence, query_reference, request_id, is_last, session_id);
    });
}

void
TdApi::OnQueryOptionCombinedOrdersByPageEx(XTPOptCombOrderInfoEx *order_info, int64_t req_count, int64_t order_sequence,
                                           int64_t query_reference, int request_id, bool is_last, uint64_t session_id) {
    bool has_data{false};
    XTPOptCombOrderInfoEx order_info_{};
    if (order_info) {
        has_data = true;
        order_info_ = *order_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_order_info{};
        if (has_data) {
            py_order_info["order_xtp_id"] = order_info_.order_xtp_id;
            py_order_info["order_client_id"] = order_info_.order_client_id;
            py_order_info["order_cancel_client_id"] = order_info_.order_cancel_client_id;
            py_order_info["order_cancel_xtp_id"] = order_info_.order_cancel_xtp_id;
            py_order_info["market"] = order_info_.market;
            py_order_info["quantity"] = order_info_.quantity;
            py_order_info["side"] = order_info_.side;
            py_order_info["business_type"] = order_info_.business_type;
            py_order_info["qty_traded"] = order_info_.qty_traded;
            py_order_info["qty_left"] = order_info_.qty_left;
            py_order_info["insert_time"] = order_info_.insert_time;
            py_order_info["update_time"] = order_info_.update_time;
            py_order_info["cancel_time"] = order_info_.cancel_time;
            py_order_info["trade_amount"] = order_info_.trade_amount;
            py_order_info["order_local_id"] = order_info_.order_local_id;
            py_order_info["order_status"] = order_info_.order_status;
            py_order_info["order_submit_status"] = order_info_.order_submit_status;
            py_order_info["order_type"] = order_info_.order_type;

            nb::dict opt_comb_info_{};
            opt_comb_info_["strategy_id"] = order_info_.opt_comb_info.strategy_id;
            opt_comb_info_["comb_num"] = order_info_.opt_comb_info.comb_num;
            opt_comb_info_["num_legs"] = order_info_.opt_comb_info.num_legs;

            nb::list leg_detail_{};
            for (int i = 0; i < order_info_.opt_comb_info.num_legs; i++) {
                nb::dict leg_{};
                leg_["leg_security_id"] = order_info_.opt_comb_info.leg_detail[i].leg_security_id;
                leg_["leg_cntr_type"] = order_info_.opt_comb_info.leg_detail[i].leg_cntr_type;
                leg_["leg_side"] = order_info_.opt_comb_info.leg_detail[i].leg_side;
                leg_["leg_covered"] = order_info_.opt_comb_info.leg_detail[i].leg_covered;
                leg_["leg_qty"] = order_info_.opt_comb_info.leg_detail[i].leg_qty;
                leg_detail_.append(leg_);
            }
            opt_comb_info_["leg_detail"] = leg_detail_;
            py_order_info["opt_comb_info"] = opt_comb_info_;

            py_order_info["order_exch_id"] = order_info_.order_exch_id;

            nb::dict order_err_t_{};
            order_err_t_["error_id"] = order_info_.order_err_t.error_id;
            order_err_t_["error_msg"] = order_info_.order_err_t.error_msg;
            py_order_info["order_err_t"] = order_err_t_;
        }
        PyOnQueryOptionCombinedOrdersByPageEx(py_order_info, req_count, order_sequence, query_reference, request_id, is_last, session_id);
    });
}

void
TdApi::OnQueryOptionCombinedTrades(XTPQueryOptCombTradeRsp *trade_info, XTPRI *error_info, int request_id, bool is_last,
                                   uint64_t session_id) {
    bool has_data{false};
    XTPQueryOptCombTradeRsp trade_info_{};
    if (trade_info) {
        has_data = true;
        trade_info_ = *trade_info;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_trade_info{};
        if (has_data) {
            py_trade_info["order_xtp_id"] = trade_info_.order_xtp_id;
            py_trade_info["order_client_id"] = trade_info_.order_client_id;
            py_trade_info["market"] = trade_info_.market;
            py_trade_info["local_order_id"] = trade_info_.local_order_id;
            py_trade_info["exec_id"] = trade_info_.exec_id;
            py_trade_info["quantity"] = trade_info_.quantity;
            py_trade_info["trade_time"] = trade_info_.trade_time;
            py_trade_info["trade_amount"] = trade_info_.trade_amount;
            py_trade_info["report_index"] = trade_info_.report_index;
            py_trade_info["order_exch_id"] = trade_info_.order_exch_id;
            py_trade_info["trade_type"] = trade_info_.trade_type;
            py_trade_info["side"] = trade_info_.side;
            py_trade_info["business_type"] = trade_info_.business_type;
            py_trade_info["branch_pbu"] = trade_info_.branch_pbu;

            nb::dict opt_comb_info_{};
            opt_comb_info_["strategy_id"] = trade_info_.opt_comb_info.strategy_id;
            opt_comb_info_["comb_num"] = trade_info_.opt_comb_info.comb_num;
            opt_comb_info_["num_legs"] = trade_info_.opt_comb_info.num_legs;

            nb::list leg_detail_{};
            for (int i = 0; i < trade_info_.opt_comb_info.num_legs; i++) {
                nb::dict leg_{};
                leg_["leg_security_id"] = trade_info_.opt_comb_info.leg_detail[i].leg_security_id;
                leg_["leg_cntr_type"] = trade_info_.opt_comb_info.leg_detail[i].leg_cntr_type;
                leg_["leg_side"] = trade_info_.opt_comb_info.leg_detail[i].leg_side;
                leg_["leg_covered"] = trade_info_.opt_comb_info.leg_detail[i].leg_covered;
                leg_["leg_qty"] = trade_info_.opt_comb_info.leg_detail[i].leg_qty;
                leg_detail_.append(leg_);
            }
            opt_comb_info_["leg_detail"] = leg_detail_;

            py_trade_info["opt_comb_info"] = opt_comb_info_;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnQueryOptionCombinedTrades(py_trade_info, py_error, request_id, is_last, session_id);
    });
}

void
TdApi::OnQueryOptionCombinedTradesByPage(XTPQueryOptCombTradeRsp *trade_info, int64_t req_count, int64_t trade_sequence,
                                         int64_t query_reference, int request_id, bool is_last, uint64_t session_id) {
    bool has_data{false};
    XTPQueryOptCombTradeRsp trade_info_{};
    if (trade_info) {
        has_data = true;
        trade_info_ = *trade_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_trade_info{};
        if (has_data) {
            py_trade_info["order_xtp_id"] = trade_info_.order_xtp_id;
            py_trade_info["order_client_id"] = trade_info_.order_client_id;
            py_trade_info["market"] = trade_info_.market;
            py_trade_info["local_order_id"] = trade_info_.local_order_id;
            py_trade_info["exec_id"] = trade_info_.exec_id;
            py_trade_info["quantity"] = trade_info_.quantity;
            py_trade_info["trade_time"] = trade_info_.trade_time;
            py_trade_info["trade_amount"] = trade_info_.trade_amount;
            py_trade_info["report_index"] = trade_info_.report_index;
            py_trade_info["order_exch_id"] = trade_info_.order_exch_id;
            py_trade_info["trade_type"] = trade_info_.trade_type;
            py_trade_info["side"] = trade_info_.side;
            py_trade_info["business_type"] = trade_info_.business_type;
            py_trade_info["branch_pbu"] = trade_info_.branch_pbu;

            nb::dict opt_comb_info_{};
            opt_comb_info_["strategy_id"] = trade_info_.opt_comb_info.strategy_id;
            opt_comb_info_["comb_num"] = trade_info_.opt_comb_info.comb_num;
            opt_comb_info_["num_legs"] = trade_info_.opt_comb_info.num_legs;

            nb::list leg_detail_{};
            for (int i = 0; i < trade_info_.opt_comb_info.num_legs; i++) {
                nb::dict leg_{};
                leg_["leg_security_id"] = trade_info_.opt_comb_info.leg_detail[i].leg_security_id;
                leg_["leg_cntr_type"] = trade_info_.opt_comb_info.leg_detail[i].leg_cntr_type;
                leg_["leg_side"] = trade_info_.opt_comb_info.leg_detail[i].leg_side;
                leg_["leg_covered"] = trade_info_.opt_comb_info.leg_detail[i].leg_covered;
                leg_["leg_qty"] = trade_info_.opt_comb_info.leg_detail[i].leg_qty;
                leg_detail_.append(leg_);
            }
            opt_comb_info_["leg_detail"] = leg_detail_;

            py_trade_info["opt_comb_info"] = opt_comb_info_;
        }
        PyOnQueryOptionCombinedTradesByPage(py_trade_info, req_count, trade_sequence, query_reference, request_id, is_last, session_id);
    });
}

void TdApi::OnQueryOptionCombinedPosition(XTPQueryOptCombPositionRsp *position_info, XTPRI *error_info, int request_id,
                                          bool is_last, uint64_t session_id) {
    bool has_data{false};
    XTPQueryOptCombPositionRsp position_info_{};
    if (position_info) {
        has_data = true;
        position_info_ = *position_info;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_position_info{};
        if (has_data) {
            py_position_info["strategy_id"] = position_info_.strategy_id;
            py_position_info["strategy_name"] = position_info_.strategy_name;
            py_position_info["market"] = position_info_.market;
            py_position_info["total_qty"] = position_info_.total_qty;
            py_position_info["available_qty"] = position_info_.available_qty;
            py_position_info["yesterday_position"] = position_info_.yesterday_position;

            nb::dict opt_comb_info_{};
            opt_comb_info_["strategy_id"] = position_info_.opt_comb_info.strategy_id;
            opt_comb_info_["comb_num"] = position_info_.opt_comb_info.comb_num;
            opt_comb_info_["num_legs"] = position_info_.opt_comb_info.num_legs;

            nb::list leg_detail_{};
            for (int i = 0; i < position_info_.opt_comb_info.num_legs; i++) {
                nb::dict leg_{};
                leg_["leg_security_id"] = position_info_.opt_comb_info.leg_detail[i].leg_security_id;
                leg_["leg_cntr_type"] = position_info_.opt_comb_info.leg_detail[i].leg_cntr_type;
                leg_["leg_side"] = position_info_.opt_comb_info.leg_detail[i].leg_side;
                leg_["leg_covered"] = position_info_.opt_comb_info.leg_detail[i].leg_covered;
                leg_["leg_qty"] = position_info_.opt_comb_info.leg_detail[i].leg_qty;
                leg_detail_.append(leg_);
            }
            opt_comb_info_["leg_detail"] = leg_detail_;
            py_position_info["opt_comb_info"] = opt_comb_info_;

            py_position_info["secu_comb_margin"] = position_info_.secu_comb_margin;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnQueryOptionCombinedPosition(py_position_info, py_error, request_id, is_last, session_id);
    });
}

void TdApi::OnQueryOptionCombinedStrategyInfo(XTPQueryCombineStrategyInfoRsp *strategy_info, XTPRI *error_info,
                                              int request_id, bool is_last, uint64_t session_id) {
    bool has_data{false};
    XTPQueryCombineStrategyInfoRsp strategy_info_{};
    if (strategy_info) {
        has_data = true;
        strategy_info_ = *strategy_info;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_strategy_info{};
        if (has_data) {
            py_strategy_info["strategy_id"] = strategy_info_.strategy_id;
            py_strategy_info["strategy_name"] = strategy_info_.strategy_name;
            py_strategy_info["market"] = strategy_info_.market;
            py_strategy_info["leg_num"] = strategy_info_.leg_num;

            nb::list leg_strategy_{};
            for (int i = 0; i < strategy_info_.leg_num; i++) {
                nb::dict strategy_{};
                strategy_["call_or_put"] = strategy_info_.leg_strategy[i].call_or_put;
                strategy_["position_side"] = strategy_info_.leg_strategy[i].position_side;
                strategy_["exercise_price_seq"] = strategy_info_.leg_strategy[i].exercise_price_seq;
                strategy_["expire_date_seq"] = strategy_info_.leg_strategy[i].expire_date_seq;
                strategy_["leg_qty"] = strategy_info_.leg_strategy[i].leg_qty;
                leg_strategy_.append(strategy_);
            }
            py_strategy_info["leg_strategy"] = leg_strategy_;
            py_strategy_info["expire_date_type"] = strategy_info_.expire_date_type;
            py_strategy_info["underlying_type"] = strategy_info_.underlying_type;
            py_strategy_info["auto_sep_type"] = strategy_info_.auto_sep_type;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnQueryOptionCombinedStrategyInfo(py_strategy_info, py_error, request_id, is_last, session_id);
    });
}

void
TdApi::OnQueryOptionCombinedExecPosition(XTPQueryOptCombExecPosRsp *position_info, XTPRI *error_info, int request_id,
                                         bool is_last, uint64_t session_id) {
    bool has_data{false};
    XTPQueryOptCombExecPosRsp position_info_{};
    if (position_info) {
        has_data = true;
        position_info_ = *position_info;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_position_info{};
        if (has_data) {
            py_position_info["market"] = position_info_.market;
            py_position_info["cntrt_code_1"] = position_info_.cntrt_code_1;
            py_position_info["cntrt_name_1"] = position_info_.cntrt_name_1;
            py_position_info["position_side_1"] = position_info_.position_side_1;
            py_position_info["call_or_put_1"] = position_info_.call_or_put_1;
            py_position_info["avl_qty_1"] = position_info_.avl_qty_1;
            py_position_info["orig_own_qty_1"] = position_info_.orig_own_qty_1;
            py_position_info["own_qty_1"] = position_info_.own_qty_1;
            py_position_info["cntrt_code_2"] = position_info_.cntrt_code_2;
            py_position_info["cntrt_name_2"] = position_info_.cntrt_name_2;
            py_position_info["position_side_2"] = position_info_.position_side_2;
            py_position_info["call_or_put_2"] = position_info_.call_or_put_2;
            py_position_info["avl_qty_2"] = position_info_.avl_qty_2;
            py_position_info["orig_own_qty_2"] = position_info_.orig_own_qty_2;
            py_position_info["own_qty_2"] = position_info_.own_qty_2;
            py_position_info["net_qty"] = position_info_.net_qty;
            py_position_info["order_qty"] = position_info_.order_qty;
            py_position_info["confirm_qty"] = position_info_.confirm_qty;
            py_position_info["avl_qty"] = position_info_.avl_qty;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnQueryOptionCombinedExecPosition(py_position_info, py_error, request_id, is_last, session_id);
    });
}

void TdApi::OnQueryStrategy(XTPStrategyInfoStruct *strategy_info, char *strategy_param, XTPRI *error_info,
                            int32_t request_id, bool is_last, uint64_t session_id) {
    bool has_data{false};
    XTPStrategyInfoStruct strategy_info_{};
    if (strategy_info) {
        has_data = true;
        strategy_info_ = *strategy_info;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_strategy_info{};
        if (has_data) {
            py_strategy_info["m_strategy_type"] = strategy_info_.m_strategy_type;
            py_strategy_info["m_strategy_state"] = strategy_info_.m_strategy_state;
            py_strategy_info["m_client_strategy_id"] = strategy_info_.m_client_strategy_id;
            py_strategy_info["m_xtp_strategy_id"] = strategy_info_.m_xtp_strategy_id;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnQueryStrategy(py_strategy_info, strategy_param, py_error, request_id, is_last, session_id);
    });
}

void TdApi::OnStrategyStateReport(XTPStrategyStateReportStruct *strategy_state, uint64_t session_id) {
    bool has_data{false};
    XTPStrategyStateReportStruct strategy_state_{};
    if (strategy_state) {
        has_data = true;
        strategy_state_ = *strategy_state;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_strategy_state{};
        if (has_data) {
            nb::dict m_strategy_info_{};
            m_strategy_info_["m_strategy_type"] = strategy_state_.m_strategy_info.m_strategy_type;
            m_strategy_info_["m_strategy_state"] = strategy_state_.m_strategy_info.m_strategy_state;
            m_strategy_info_["m_client_strategy_id"] = strategy_state_.m_strategy_info.m_client_strategy_id;
            m_strategy_info_["m_xtp_strategy_id"] = strategy_state_.m_strategy_info.m_xtp_strategy_id;
            py_strategy_state["m_strategy_info"] = m_strategy_info_;
            py_strategy_state["m_strategy_qty"] = strategy_state_.m_strategy_qty;
            py_strategy_state["m_strategy_ordered_qty"] = strategy_state_.m_strategy_ordered_qty;
            py_strategy_state["m_strategy_cancelled_qty"] = strategy_state_.m_strategy_cancelled_qty;
            py_strategy_state["m_strategy_execution_qty"] = strategy_state_.m_strategy_execution_qty;
            py_strategy_state["m_strategy_unclosed_qty"] = strategy_state_.m_strategy_unclosed_qty;
            py_strategy_state["m_strategy_asset"] = strategy_state_.m_strategy_asset;
            py_strategy_state["m_strategy_ordered_asset"] = strategy_state_.m_strategy_ordered_asset;
            py_strategy_state["m_strategy_execution_asset"] = strategy_state_.m_strategy_execution_asset;
            py_strategy_state["m_strategy_execution_price"] = strategy_state_.m_strategy_execution_price;
            py_strategy_state["m_strategy_market_price"] = strategy_state_.m_strategy_market_price;
            py_strategy_state["m_strategy_price_diff"] = strategy_state_.m_strategy_price_diff;
            py_strategy_state["m_strategy_asset_diff"] = strategy_state_.m_strategy_asset_diff;

            nb::dict m_error_info_{};
            m_error_info_["error_id"] = strategy_state_.m_error_info.error_id;
            m_error_info_["error_msg"] = strategy_state_.m_error_info.error_msg;
            py_strategy_state["m_error_info"] = m_error_info_;
        }
        PyOnStrategyStateReport(py_strategy_state, session_id);
    });
}

void TdApi::OnALGOUserEstablishChannel(char *user, XTPRI *error_info, uint64_t session_id) {
    bool has_data{false};
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnALGOUserEstablishChannel(user, py_error, session_id);
    });
}

void TdApi::OnInsertAlgoOrder(XTPStrategyInfoStruct *strategy_info, XTPRI *error_info, uint64_t session_id) {
    bool has_data{false};
    XTPStrategyInfoStruct strategy_info_{};
    if (strategy_info) {
        has_data = true;
        strategy_info_ = *strategy_info;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_strategy_info{};
        if (has_data) {
            py_strategy_info["m_strategy_type"] = strategy_info_.m_strategy_type;
            py_strategy_info["m_strategy_state"] = strategy_info_.m_strategy_state;
            py_strategy_info["m_client_strategy_id"] = strategy_info_.m_client_strategy_id;
            py_strategy_info["m_xtp_strategy_id"] = strategy_info_.m_xtp_strategy_id;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnInsertAlgoOrder(py_strategy_info, py_error, session_id);
    });
}

void TdApi::OnCancelAlgoOrder(XTPStrategyInfoStruct *strategy_info, XTPRI *error_info, uint64_t session_id) {
    bool has_data{false};
    XTPStrategyInfoStruct strategy_info_{};
    if (strategy_info) {
        has_data = true;
        strategy_info_ = *strategy_info;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_strategy_info{};
        if (has_data) {
            py_strategy_info["m_strategy_type"] = strategy_info_.m_strategy_type;
            py_strategy_info["m_strategy_state"] = strategy_info_.m_strategy_state;
            py_strategy_info["m_client_strategy_id"] = strategy_info_.m_client_strategy_id;
            py_strategy_info["m_xtp_strategy_id"] = strategy_info_.m_xtp_strategy_id;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnCancelAlgoOrder(py_strategy_info, py_error, session_id);
    });
}

void TdApi::OnAlgoDisconnected(int reason) {
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        PyOnAlgoDisconnected(reason);
    });
}

void TdApi::OnAlgoConnected() {
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        PyOnAlgoConnected();
    });
}

void TdApi::OnStrategySymbolStateReport(XTPStrategySymbolStateReport *strategy_symbol_state, uint64_t session_id) {
    bool has_data{false};
    XTPStrategySymbolStateReport strategy_symbol_state_{};
    if (strategy_symbol_state) {
        has_data = true;
        strategy_symbol_state_ = *strategy_symbol_state;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_strategy_symbol_state{};
        if (has_data) {
            nb::dict m_strategy_info_{};
            m_strategy_info_["m_strategy_type"] = strategy_symbol_state_.m_strategy_info.m_strategy_type;
            m_strategy_info_["m_strategy_state"] = strategy_symbol_state_.m_strategy_info.m_strategy_state;
            m_strategy_info_["m_client_strategy_id"] = strategy_symbol_state_.m_strategy_info.m_client_strategy_id;
            m_strategy_info_["m_xtp_strategy_id"] = strategy_symbol_state_.m_strategy_info.m_xtp_strategy_id;
            py_strategy_symbol_state["m_strategy_info"] = m_strategy_info_;

            py_strategy_symbol_state["m_ticker"] = strategy_symbol_state_.m_ticker;
            py_strategy_symbol_state["m_market"] = strategy_symbol_state_.m_market;
            py_strategy_symbol_state["m_side"] = strategy_symbol_state_.m_side;
            py_strategy_symbol_state["m_strategy_qty"] = strategy_symbol_state_.m_strategy_qty;
            py_strategy_symbol_state["m_strategy_ordered_qty"] = strategy_symbol_state_.m_strategy_ordered_qty;
            py_strategy_symbol_state["m_strategy_cancelled_qty"] = strategy_symbol_state_.m_strategy_cancelled_qty;
            py_strategy_symbol_state["m_strategy_execution_qty"] = strategy_symbol_state_.m_strategy_execution_qty;
            py_strategy_symbol_state["m_strategy_buy_qty"] = strategy_symbol_state_.m_strategy_buy_qty;
            py_strategy_symbol_state["m_strategy_sell_qty"] = strategy_symbol_state_.m_strategy_sell_qty;
            py_strategy_symbol_state["m_strategy_unclosed_qty"] = strategy_symbol_state_.m_strategy_unclosed_qty;
            py_strategy_symbol_state["m_strategy_asset"] = strategy_symbol_state_.m_strategy_asset;
            py_strategy_symbol_state["m_strategy_ordered_asset"] = strategy_symbol_state_.m_strategy_ordered_asset;
            py_strategy_symbol_state["m_strategy_execution_asset"] = strategy_symbol_state_.m_strategy_execution_asset;
            py_strategy_symbol_state["m_strategy_buy_asset"] = strategy_symbol_state_.m_strategy_buy_asset;
            py_strategy_symbol_state["m_strategy_sell_asset"] = strategy_symbol_state_.m_strategy_sell_asset;
            py_strategy_symbol_state["m_strategy_unclosed_asset"] = strategy_symbol_state_.m_strategy_unclosed_asset;
            py_strategy_symbol_state["m_strategy_asset_diff"] = strategy_symbol_state_.m_strategy_asset_diff;
            py_strategy_symbol_state["m_strategy_execution_price"] = strategy_symbol_state_.m_strategy_execution_price;
            py_strategy_symbol_state["m_strategy_market_price"] = strategy_symbol_state_.m_strategy_market_price;
            py_strategy_symbol_state["m_strategy_price_diff"] = strategy_symbol_state_.m_strategy_price_diff;

            nb::dict m_error_info_{};
            m_error_info_["error_id"] = strategy_symbol_state_.m_error_info.error_id;
            m_error_info_["error_msg"] = strategy_symbol_state_.m_error_info.error_msg;
            py_strategy_symbol_state["m_error_info"] = m_error_info_;
        }
        PyOnStrategySymbolStateReport(py_strategy_symbol_state, session_id);
    });
}

void TdApi::OnNewStrategyCreateReport(XTPStrategyInfoStruct *strategy_info, char *strategy_param, uint64_t session_id) {
    bool has_data{false};
    XTPStrategyInfoStruct strategy_info_{};
    if (strategy_info) {
        has_data = true;
        strategy_info_ = *strategy_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_strategy_info{};
        if (has_data) {
            py_strategy_info["m_strategy_type"] = strategy_info_.m_strategy_type;
            py_strategy_info["m_strategy_state"] = strategy_info_.m_strategy_state;
            py_strategy_info["m_client_strategy_id"] = strategy_info_.m_client_strategy_id;
            py_strategy_info["m_xtp_strategy_id"] = strategy_info_.m_xtp_strategy_id;
        }
        PyOnNewStrategyCreateReport(py_strategy_info, strategy_param, session_id);
    });
}

void TdApi::OnStrategyRecommendation(bool basket_flag, XTPStrategyRecommendationInfo *recommendation_info,
                                     char *strategy_param, XTPRI *error_info, int32_t request_id, bool is_last,
                                     uint64_t session_id) {
    bool has_data{false};
    XTPStrategyRecommendationInfo recommendation_info_{};
    if (recommendation_info) {
        has_data = true;
        recommendation_info_ = *recommendation_info;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_recommendation_info{};
        if (has_data) {
            py_recommendation_info["m_strategy_type"] = recommendation_info_.m_strategy_type;
            py_recommendation_info["m_market"] = recommendation_info_.m_market;
            py_recommendation_info["m_ticker"] = recommendation_info_.m_ticker;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnStrategyRecommendation(basket_flag, py_recommendation_info, strategy_param, py_error, request_id, is_last, session_id);
    });
}
