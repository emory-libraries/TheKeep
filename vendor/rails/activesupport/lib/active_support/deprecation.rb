module ActiveSupport
  module Deprecation
    # Choose the default warn behavior according to RAILS_ENV.
    # Ignore deprecation warnings in production.
    DEFAULT_BEHAVIORS = {
      'test'        => Proc.new { |message| $stderr.puts message },
      'development' => Proc.new { |message| RAILS_DEFAULT_LOGGER.warn message },
    }

    class << self
      def warn(message = nil, callstack = caller)
        behavior.call(deprecation_message(callstack, message)) if behavior
      end

      def default_behavior
        DEFAULT_BEHAVIORS[RAILS_ENV.to_s] if defined?(RAILS_ENV)
      end

      private
        def deprecation_message(callstack, message = nil)
          file, line, method = extract_callstack(callstack)
          message ||= "WARNING: #{method} is deprecated and will be removed from the next Rails release"
          "#{message} (#{method} at #{file}:#{line})"
        end

        def extract_callstack(callstack)
          callstack.first.match(/^(.+?):(\d+)(?::in `(.*?)')?/).captures
        end
    end

    # Behavior is a block that takes a message argument.
    mattr_accessor :behavior
    self.behavior = default_behavior

    module ClassMethods
      # Declare that a method has been deprecated.
      def deprecate(*method_names)
        method_names.each do |method_name|
          class_eval(<<-EOS, __FILE__, __LINE__)
            def #{method_name}_with_deprecation(*args, &block)
              ::ActiveSupport::Deprecation.warn
              #{method_name}_without_deprecation(*args, &block)
            end
          EOS
          alias_method_chain(method_name, :deprecation)
        end
      end
    end

    module Assertions
      def assert_deprecated(match = nil, &block)
        last = collect_deprecations(&block).last
        assert last, "Expected a deprecation warning within the block but received none"
        if match
          match = Regexp.new(Regexp.escape(match)) unless match.is_a?(Regexp)
          assert_match match, last, "Deprecation warning didn't match #{match}: #{last}"
        end
      end

      def assert_not_deprecated(&block)
        deprecations = collect_deprecations(&block)
        assert deprecations.empty?, "Expected no deprecation warning within the block but received #{deprecations.size}: \n  #{deprecations * "\n  "}"
      end

      private
        
        def collect_deprecations
          old_behavior = ActiveSupport::Deprecation.behavior
          deprecations = []
          ActiveSupport::Deprecation.behavior = Proc.new do |message|
            deprecations << message
            old_behavior.call(message) if old_behavior
          end
          yield
          return deprecations
        ensure
          ActiveSupport::Deprecation.behavior = old_behavior
        end
    end

    # Stand-in for @request, @attributes, etc.
    class DeprecatedInstanceVariableProxy
      instance_methods.each { |m| undef_method m unless m =~ /^__/ }

      def initialize(instance, method, var = "@#{method}")
        @instance, @method, @var = instance, method, var
      end

      private
        def warn(callstack, called, args)
          ActiveSupport::Deprecation.warn("#{@var} is deprecated! Call #{@method}.#{called} instead of #{@var}.#{called}. Args: #{args.inspect}", callstack)
        end

        def method_missing(called, *args, &block)
          warn caller, called, args
          @instance.__send__(@method).__send__(called, *args, &block)
        end
    end
  end
end

class Class
  include ActiveSupport::Deprecation::ClassMethods
end

module Test
  module Unit
    class TestCase
      include ActiveSupport::Deprecation::Assertions
    end
  end
end
