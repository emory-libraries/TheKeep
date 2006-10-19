class AccessRight < ActiveRecord::Base
  belongs_to :content
  belongs_to :name
  belongs_to :restriction
end
