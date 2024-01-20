export interface AccountResponse {
    success: boolean;
    data: {
      account_data: AccountData,
      transaction_history: TransactionData[]
    },
    message?: string
  }

export interface CreateAccountResponse {
  success: boolean;
  message: string;
}

  interface AccountData {
    _links: {
      self: {
        href: string;
      };
      transactions: {
        href: string;
        templated: boolean;
      };
      operations: {
        href: string;
        templated: boolean;
      };
      payments: {
        href: string;
        templated: boolean;
      };
      effects: {
        href: string;
        templated: boolean;
      };
      offers: {
        href: string;
        templated: boolean;
      };
      trades: {
        href: string;
        templated: boolean;
      };
      data: {
        href: string;
        templated: boolean;
      };
    };
    id: string;
    account_id: string;
    sequence: string;
    sequence_ledger: number;
    sequence_time: string;
    subentry_count: number;
    last_modified_ledger: number;
    last_modified_time: string;
    thresholds: {
      low_threshold: number;
      med_threshold: number;
      high_threshold: number;
    };
    flags: {
      auth_required: boolean;
      auth_revocable: boolean;
      auth_immutable: boolean;
      auth_clawback_enabled: boolean;
    };
    balances: Array<{
      balance: string;
      buying_liabilities: string;
      selling_liabilities: string;
      asset_type: string;
    }>;
    signers: Array<{
      weight: number;
      key: string;
      type: string;
    }>;
    data: Record<string, unknown>;
    num_sponsoring: number;
    num_sponsored: number;
    paging_token: string;
  }
  export interface AuthResponse {
    success: boolean;
    data: {
      token: string;
      email: string;
    };
    message: string;
  }

  interface TransactionData {
    id: string;
    paging_token: string;
    successful: boolean;
    created_at: string;
    source_account: string;
    fee_account: string;
    fee_charged: string;
    operation_count: number;
    memo_type: string;
    memo?: string;
  }
  