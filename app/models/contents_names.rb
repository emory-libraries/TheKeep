class ContentsNames < ActiveRecord::Base
  belongs_to :content
  belongs_to :name
  belongs_to :role
  
end
